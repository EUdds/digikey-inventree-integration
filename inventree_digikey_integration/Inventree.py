from inventree.company import SupplierPart, Company, ManufacturerPart
from inventree.part import Part, PartCategory
from inventree.base import InventreeObject

from .suppliers import DigikeyPart
from .suppliers.SupplierBase import SupplierPartBase
from .ImageManager import ImageManager
from .ConfigReader import ConfigReader


class InventreePart:
    def __init__(self, supplier_part_number, supplier):
        self.supplier_part_number = supplier_part_number
        self.supplier = supplier

    def import_part_from_supplier(self, config: ConfigReader, prompt=False):
        for supplier in SupplierPartBase.__subclasses__():
            if supplier.SUPPLIER_NAME == self.supplier:
                self.supplier_part = supplier.from_supplier_part_number(
                    self.supplier_part_number, config, prompt=prompt
                )
                break
        else:
            raise ValueError(f"Unknown supplier {self.supplier}")

    def get_supplier(self, config: ConfigReader):
        suppliers = Company.list(config.inventree_api, name=self.supplier)
        if len(suppliers) == 0:
            supplier = Company.create(
                config.inventree_api,
                {
                    "name": f"{self.supplier}",
                    "is_supplier": True,
                    "description": f"Automatically created supplier for {self.supplier}",
                },
            )
            return supplier

        return suppliers[0]

    def create_inventree_part(self, config: ConfigReader):
        category = find_category(config)
        possible_parts = Part.list(
            config.inventree_api,
            name=self.supplier_part.name,
            description=self.supplier_part.description,
        )
        if len(possible_parts) > 0:
            part_names = [p.name.lower() for p in possible_parts]
            if self.supplier_part.name.lower() in part_names:
                print("Part already exists")
                existing_part = possible_parts[
                    part_names.index(self.supplier_part.name.lower())
                ]
                return existing_part

        part = Part.create(
            config.inventree_api,
            {
                "name": self.supplier_part.name,
                "description": self.supplier_part.description,
                "category": category,
                "active": True,
                "virtual": False,
                "component": True,
                "purchaseable": 1,
            },
        )
        upload_picture(self.supplier_part, part)
        return part

    def create_manufacturer_part(self, config: ConfigReader, base_pk: int):
        mfg = find_manufacturer(self.supplier_part, config)
        supplier_pk = int(self.get_supplier(config).pk)
        mfg_part = ManufacturerPart.create(
            config.inventree_api,
            {
                "part": base_pk,
                "supplier": supplier_pk,
                "MPN": self.supplier_part.mfg_part_num,
                "manufacturer": mfg.pk,
            },
        )
        return mfg_part

    def create_supplier_part(self, config: ConfigReader, base_pk: int, mfg_pk: int):
        supplier_part = SupplierPart.create(
            config.inventree_api,
            {
                "part": base_pk,
                "supplier": self.get_supplier_pk(config),
                "SKU": self.supplier_part.supplier_part_num,
                "manufacturer": mfg_pk,
                "description": self.supplier_part.description,
                "link": self.supplier_part.link,
            },
        )
        return supplier_part.pk

    def add_to_inventree(self, config: ConfigReader):
        inv_part = self.create_inventree_part(config)
        inv_pk = int(inv_part.pk)
        mfg_part_pk = int(self.create_manufacturer_part(config, inv_pk).pk)
        supplier_part_pk = self.create_supplier_part(config, inv_pk, mfg_part_pk)
        return supplier_part_pk


def create_inventree_part(dkpart: DigikeyPart, config: ConfigReader):
    category = find_category(config)
    possible_parts = Part.list(
        config.inventree_api, name=dkpart.name, description=dkpart.description
    )
    if len(possible_parts) > 0:
        part_names = [p.name.lower() for p in possible_parts]
        if dkpart.name.lower() in part_names:
            print("Part already exists")
            return possible_parts[part_names.index(dkpart.name.lower())]
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


def find_manufacturer(dkpart: DigikeyPart, config: ConfigReader):
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


def upload_picture(dkpart: DigikeyPart, invPart):
    if dkpart.picture is not None:
        img_file = ImageManager.get_image(dkpart.picture)
        invPart.uploadImage(img_file)
        ImageManager.clean_cache()
