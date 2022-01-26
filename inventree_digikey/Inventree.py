import configparser
import time


from inventree.api import InvenTreeAPI
from inventree.company import SupplierPart, Company
from inventree.part import Part, PartCategory
from inventree.base import Parameter, ParameterTemplate
from pathlib import Path

from .Digikey import DigiPart
from .ImageManager import ImageManager

config = configparser.ConfigParser()
config_path = Path(__file__).resolve().parent / "config.ini"
config.read(config_path)

API_URL = config['INVENTREE_API']['URL']
USERNAME = config['INVENTREE_API']['USER']
PASSWORD = config['INVENTREE_API']['PASSWORD']

API = InvenTreeAPI(API_URL, username=USERNAME, password=PASSWORD)


def add_digikey_part(dkpart: DigiPart):
    dk = get_digikey_supplier()
    inv_part = create_inventree_part(dkpart)
    if inv_part == -1:
        return
    base_pk = int(inv_part.pk)
    mfg = find_manufacturer(dkpart)
    SupplierPart.create(API, {
            "part":base_pk,
            "supplier": dk.pk,
            "SKU": dkpart.digi_part_num,
            "manufacturer": mfg.pk,
            "description": dkpart.description,
            "MPN": dkpart.mfg_part_num,
            "link": dkpart.link
            })
    return

def get_digikey_supplier():
    dk = Company.list(API, name="Digikey")
    return dk[0]

def create_inventree_part(dkpart: DigiPart):
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
    categories = PartCategory.list(API)
    print("="*20)
    print("Choose a category")
    for idx, category in enumerate(categories):
        print("\t%d %s" %(idx, category.name))
    print("="*20)
    idx = int(input("> "))
    return categories[idx]

def find_manufacturer(dkpart: DigiPart):
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
        invPart.upload_image(img_file)
        ImageManager.clean_cache()
