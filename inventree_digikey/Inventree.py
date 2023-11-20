import configparser
import os

from inventree.api import InvenTreeAPI
from inventree.company import SupplierPart, Company, ManufacturerPart
from inventree.part import Part, PartCategory, Parameter, ParameterTemplate
from inventree.order import PurchaseOrderLineItem, PurchaseOrder

from pathlib import Path

from .Digikey import DigiPart, DigiOrder, get_part_from_part_number
from .ImageManager import ImageManager

if "DIGIKEY_INVENTREE_TEST_MODE" in os.environ:
    CONFIG_FILE_PATH = os.environ["DIGIKEY_INVENTREE_TEST_CONFIG_PATH"]
else:
    CONFIG_FILE_PATH = Path(__file__).resolve().parent / "config.ini"

API_URL = None
USERNAME = None
PASSWORD = None
API = None

def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    global API_URL, USERNAME, PASSWORD, API

    API_URL = config['INVENTREE_API']['URL']
    USERNAME = config['INVENTREE_API']['USER']
    PASSWORD = config['INVENTREE_API']['PASSWORD']
    API = InvenTreeAPI(API_URL, username=USERNAME, password=PASSWORD)

catagory_map = {}
params_map = {}
htsus_pk = None

inventree_params = ParameterTemplate.list(API)
#for param in inventree_params:
#    print(f"{param.pk} : {param.name}")

for param in config['PARAMETERS']:
    value = config['PARAMETERS'][param]
    match_param = [p.pk for p in inventree_params if p.name == value]
    if len(match_param) > 0:
        #print(f"Found {value} in inventree with pk {match_param[0]}")
        params_map[param] = match_param[0]

# If setting say to import HTSUS, we assume inventree has a HTSUS category
if config['SETTINGS'].getboolean('IMPORT_HTSUS'):
    htsus_pk = [p.pk for p in inventree_params if p.name == "HTSUS"][0]

inventree_categories = PartCategory.list(API)
#for cat in inventree_categories:
#    print(f"{cat.pk} : {cat.name}")

for cat in config['CATEGORIES']:
    value = config['CATEGORIES'][cat]
    match_cat = [c.pk for c in inventree_categories if c.name == value]
    if len(match_cat) > 0:
        #print(f"Found {value} in inventree with pk {match_cat[0]}")
        catagory_map[cat] = match_cat[0]


def import_digikey_part(partnum: str, prompt=False):
    dkpart = get_part_from_part_number(partnum, prompt)
    return add_digikey_part(dkpart)

def add_digikey_part(dkpart: DigiPart):
    if API is None:
        load_config()
    dk = get_digikey_supplier()
    inv_part = create_inventree_part(dkpart)
    if inv_part == -1:
        return
    base_pk = int(inv_part.pk)
    mfg = find_manufacturer(dkpart)

    ManufacturerPart.create(API, {
        'part': base_pk,
        'supplier': dk.pk,
        'MPN': dkpart.mfg_part_num,
        'manufacturer': mfg.pk
        })

    return SupplierPart.create(API, {
            "part":base_pk,
            "supplier": dk.pk,
            "SKU": dkpart.digi_part_num,
            "manufacturer": mfg.pk,
            "description": dkpart.description,
            "link": dkpart.link
            })


def get_digikey_supplier():
    if API is None:
        load_config()
    dk = Company.list(API, name="Digikey")
    if len(dk) == 0:
        dk = Company.create(API, {
            'name': 'Digikey',
            'is_supplier': True,
            'description': 'Electronics Supply Store'
        })
        return dk
    else:
        return dk[0]


def create_inventree_part(dkpart: DigiPart):
    if API is None:
        load_config()
    category = find_category(dkpart)
    possible_parts = Part.list(API, name=dkpart.name, description=dkpart.description)
    if len(possible_parts) > 0:
        part_names = [p.name.lower() for p in possible_parts]
        if dkpart.name.lower() in part_names:
            print("Part already exists")
            return -1
    part = Part.create(API, {
        'name': dkpart.name,
        'description': dkpart.description,
        'category': category,
        'active': True,
        'virtual': False,
        'component': True,
        'purchaseable': 1
        })
    upload_picture(dkpart, part)
    set_parameters(dkpart, part)
    return part


def find_category(dkpart: DigiPart):
    if API is None:
        load_config()
    if str.lower(dkpart.category) in catagory_map:
        return catagory_map[str.lower(dkpart.category)]
    else:
        categories = PartCategory.list(API)
        print("="*20)
        print(f"Choose a category for {dkpart.category}")
        for idx, category in enumerate(categories):
            print("\t%d %s" %(idx, category.name))
        print("="*20)
        idx = int(input("> "))
        return categories[idx].pk


def find_manufacturer(dkpart: DigiPart):
    if API is None:
        load_config()
    possible_manufacturers = Company.list(API, name=dkpart.manufacturer)
    if len(possible_manufacturers) == 0:
        mfg = create_manufacturer(dkpart.manufacturer)
        return mfg
    elif len(possible_manufacturers) == 1:
        return possible_manufacturers[0]
    else:
        print("="*20)
        print("Choose a manufacturer")
        for idx, mfg in enumerate(possible_manufacturers):
            print("\t%d %s" %(idx, mfg.name, ))
        print("="*20)
        idx = int(input("> "))
        return possible_manufacturers[idx]


def create_manufacturer(name: str, is_supplier: bool=False):
    if API is None:
        load_config()
    mfg = Company.create(API, {
        'name': name,
        'is_manufacturer': True,
        'is_supplier': is_supplier,
        'description': name
        })
    return mfg

def upload_picture(dkpart: DigiPart, invPart):
    if dkpart.picture is not None:
        img_file = ImageManager.get_image(dkpart.picture)
        invPart.uploadImage(img_file)
        ImageManager.clean_cache()


def set_parameters(pkpart: DigiPart, invPart):
    #print(params_map)
    # set HTSUS code if we have a pk for this setting
    if htsus_pk:
        print(f"Importing HTSUS code {pkpart.htsus}")
        Parameter.create(API, {
            'part': invPart.pk,
            'template': htsus_pk,
            'data': pkpart.htsus
        })
    # Iterate over all the parameters and set them if they are in the config file
    for param in pkpart.parameters:
        #print(f"Getting parameter from digikey {param[0]} with value {param[1]}")
        if str.lower(param[0]) in params_map:
            template = params_map[str.lower(param[0])]
            print(f"Setting {param[0]} to {param[1]}")
            Parameter.create(API, {
                'part': invPart.pk,
                'template': template,
                'data': param[1]
            })
        #else:
        #    print(f"Could not find parameter {param[0]} in inventree")


def add_digikey_order(order: DigiOrder):
    dk = get_digikey_supplier()
    po = dk.createPurchaseOrder(supplier_reference=order.order_number)
    print(f"Created PO {po.reference} for order {order.order_number}")
    for line_item in order.line_items:
        print(line_item.digi_key_part_number)
        part = dk.getSuppliedParts(SKU=line_item.digi_key_part_number)
        if len(part) == 0:
            part = [import_digikey_part(line_item.digi_key_part_number)]
            if part:
                print(f"Warning: Could not find part, importing it {line_item.digi_key_part_number}")
            else:
                print(f"ERROR: Could not find part, and could not import it {line_item.digi_key_part_number}")
                exit(1)
        elif len(part) > 1:
            print(f"ERROR: Found multiple parts with SKU {line_item.digi_key_part_number}")
            exit(1)

        print(f"Part {part[0].SKU} has pk {part[0].pk}")
        po.addLineItem(
            part=part[0].pk,
            quantity=line_item.quantity,
            purchase_price=line_item.unit_price,
            notes=f"Invoice: {line_item.invoice_id}"
        )
    po.issue()
    return po
