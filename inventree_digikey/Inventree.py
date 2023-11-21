import configparser
import os

from inventree.api import InvenTreeAPI
from inventree.company import SupplierPart, Company, ManufacturerPart
from inventree.part import Part, PartCategory, Parameter, ParameterTemplate
from pathlib import Path

from .Digikey import DigiPart
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

    SupplierPart.create(API, {
            "part":base_pk,
            "supplier": dk.pk,
            "SKU": dkpart.digi_part_num,
            "manufacturer": mfg.pk,
            "description": dkpart.description,
            "link": dkpart.link
            })
    
    return


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
    category = find_category()
    possible_parts = Part.list(API, name=dkpart.name, description=dkpart.description)
    if len(possible_parts) > 0:
        part_names = [p.name.lower() for p in possible_parts]
        if dkpart.name.lower() in part_names:
            print("Part already exists")
            return -1
    part = Part.create(API, {
        'name': dkpart.name,
        'description': dkpart.description,
        'category': category.pk,
        'active': True,
        'virtual': False,
        'component': True,
        'purchaseable': 1
        })
    upload_picture(dkpart, part)
    return part


def find_category():
    if API is None:
        load_config()
    categories = PartCategory.list(API)
    print("="*20)
    print("Choose a category")
    for idx, category in enumerate(categories):
        print("\t%d %s" %(idx, category.name))
    print("="*20)
    idx = int(input("> "))
    return categories[idx]

def find_manufacturer(dkpart: DigiPart):
    if API is None:
        load_config()
    possible_manufacturers = Company.list(API, name=dkpart.manufacturer)
    if len(possible_manufacturers) == 0:
        mfg = create_manufacturer(dkpart.manufacturer)
        return mfg
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
