from inventree.company import SupplierPart, Company, ManufacturerPart
from inventree.part import Part, PartCategory

from .Digikey import DigiPart
from .ImageManager import ImageManager
from .ConfigReader import ConfigReader


def import_digikey_part(partnum: str, prompt=False):
    dkpart = DigiPart.from_digikey_part_number(
        partnum, injest_api_automatically=True, prompt=prompt
    )
    return add_digikey_part(dkpart)


def add_digikey_part(dkpart: DigiPart, config: ConfigReader):
    dk = get_digikey_supplier(config)
    inv_part = create_inventree_part(dkpart, config)
    if inv_part == -1:
        return
    base_pk = int(inv_part.pk)
    mfg = find_manufacturer(dkpart, config)

    ManufacturerPart.create(
        config.inventree_api,
        {
            "part": base_pk,
            "supplier": dk.pk,
            "MPN": dkpart.mfg_part_num,
            "manufacturer": mfg.pk,
        },
    )

    return SupplierPart.create(
        config.inventree_api,
        {
            "part": base_pk,
            "supplier": dk.pk,
            "SKU": dkpart.digi_part_num,
            "manufacturer": mfg.pk,
            "description": dkpart.description,
            "link": dkpart.link,
        },
    )


def get_digikey_supplier(config: ConfigReader):
    dk = Company.list(config.inventree_api, name="Digikey")
    if len(dk) == 0:
        dk = Company.create(
            config.inventree_api,
            {
                "name": "Digikey",
                "is_supplier": True,
                "description": "Electronics Supply Store",
            },
        )
        return dk
    else:
        return dk[0]


def create_inventree_part(dkpart: DigiPart, config: ConfigReader):
    category = find_category(config)
    possible_parts = Part.list(
        config.inventree_api, name=dkpart.name, description=dkpart.description
    )
    if len(possible_parts) > 0:
        part_names = [p.name.lower() for p in possible_parts]
        if dkpart.name.lower() in part_names:
            print("Part already exists")
            return -1
    part = Part.create(
        config.inventree_api,
        {
            "name": dkpart.name,
            "description": dkpart.description,
            "category": category,
            "active": True,
            "virtual": False,
            "component": True,
            "purchaseable": 1,
        },
    )
    upload_picture(dkpart, part)
    return part


def find_category(config):
    categories = PartCategory.list(config.inventree_api)
    print("=" * 20)
    print(f"Choose a category")
    for idx, category in enumerate(categories):
        print("\t%d %s" % (idx, category.name))
    print("=" * 20)
    idx = int(input("> "))
    return categories[idx].pk


def find_manufacturer(dkpart: DigiPart, config: ConfigReader):
    possible_manufacturers = Company.list(
        config.inventree_api, name=dkpart.manufacturer
    )
    if len(possible_manufacturers) == 0:
        mfg = create_manufacturer(dkpart.manufacturer, config)
        return mfg
    else:
        print("=" * 20)
        print("Choose a manufacturer")
        for idx, mfg in enumerate(possible_manufacturers):
            print(
                "\t%d %s"
                % (
                    idx,
                    mfg.name,
                )
            )
        print("=" * 20)
        idx = int(input("> "))
        return possible_manufacturers[idx]


def create_manufacturer(name: str, config: ConfigReader, is_supplier: bool = False):
    mfg = Company.create(
        config.inventree_api,
        {
            "name": name,
            "is_manufacturer": True,
            "is_supplier": is_supplier,
            "description": name,
        },
    )
    return mfg


def upload_picture(dkpart: DigiPart, invPart):
    if dkpart.picture is not None:
        img_file = ImageManager.get_image(dkpart.picture)
        invPart.uploadImage(img_file)
        ImageManager.clean_cache()
