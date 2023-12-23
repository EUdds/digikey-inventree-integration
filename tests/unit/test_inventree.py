import pytest
import inventree_digikey_integration.Inventree as test_module
from configparser import ConfigParser
import inventree.company
import inventree.api
import digikey


def mock_create_company(*args, **kwargs):
    data = args[1]
    data["pk"] = 1
    return inventree.company.Company(args[0], data=args[1])


def mock_create_part(*args, **kwargs):
    data = args[1]
    data["pk"] = 1
    return inventree.part.Part(args[0], data=args[1])


@pytest.fixture()
def test_api(test_data, monkeypatch):
    monkeypatch.setattr(
        inventree.api.InvenTreeAPI, "connect", lambda *args, **kwargs: None
    )
    api = inventree.api.InvenTreeAPI(
        test_data["test_config"]["INVENTREE_API"]["URL"],
        username=test_data["test_config"]["INVENTREE_API"]["USER"],
        password=test_data["test_config"]["INVENTREE_API"]["PASSWORD"],
    )
    return api
    # Cleanup here as necessary


@pytest.mark.parametrize(
    "supplier_part_number,supplier,supplier_wrapper_class,mfg_part_number,mfg",
    [
        # Part Number       Supplier    Supplier Part Wrapper Class Name    MFG Part Number,    MFG
        ("296-21752-2-ND", "Digikey", "DigikeyPart", "NA555DR", "Texas Instruments"),
    ],
)
class TestInventreePart:
    def test_supplier_mapping(
        self,
        supplier_part_number,
        supplier,
        supplier_wrapper_class,
        mfg_part_number,
        mfg,
        test_data,
        monkeypatch,
    ):
        monkeypatch.setattr(
            "digikey.product_details",
            lambda x: test_data["test_api_responses"][f"{supplier}_resp"],
        )
        test_part = test_module.InventreePart(supplier_part_number, supplier)
        test_part.import_part_from_supplier(test_data["config_reader"])
        assert test_part.supplier == supplier
        assert test_part.supplier_part_number == supplier_part_number
        assert type(test_part.supplier_part).__name__ == supplier_wrapper_class

    def test_get_supplier_new_company(
        self,
        supplier_part_number,
        supplier,
        supplier_wrapper_class,
        mfg_part_number,
        mfg,
        monkeypatch,
        test_data,
    ):
        monkeypatch.setattr(
            "digikey.product_details",
            lambda x: test_data["test_api_responses"][f"{supplier}_resp"],
        )
        monkeypatch.setattr(
            "inventree.company.Company.list", lambda *args, **kwargs: []
        )
        monkeypatch.setattr(inventree.company.Company, "create", mock_create_company)

        test_part = test_module.InventreePart(supplier_part_number, supplier)
        test_part.import_part_from_supplier(test_data["config_reader"])

        test_supplier = test_part.get_supplier(test_data["config_reader"])

        assert test_supplier.pk == 1
        assert test_supplier.name == supplier
        assert test_supplier.is_supplier == True

    def test_get_supplier_existing_company(
        self,
        supplier_part_number,
        supplier,
        supplier_wrapper_class,
        mfg_part_number,
        mfg,
        monkeypatch,
        test_data,
        test_api,
    ):
        monkeypatch.setattr(
            "digikey.product_details",
            lambda x: test_data["test_api_responses"][f"{supplier}_resp"],
        )
        mock_supplier_data = {
            "pk": 1,
            "name": supplier,
            "description": supplier,
        }
        monkeypatch.setattr(
            "inventree.company.Company.list",
            lambda *args, **kwargs: [
                inventree.company.Company(test_api, data=mock_supplier_data)
            ],
        )

        test_part = test_module.InventreePart(supplier_part_number, supplier)
        test_part.import_part_from_supplier(test_data["config_reader"])

        test_supplier = test_part.get_supplier(test_data["config_reader"])

        assert test_supplier.pk == 1
        assert test_supplier.name == supplier

    def test_create_inventree_part(
        self,
        supplier_part_number,
        supplier,
        supplier_wrapper_class,
        mfg_part_number,
        mfg,
        monkeypatch,
        test_data,
        test_api,
    ):
        monkeypatch.setattr(
            "inventree.part.PartCategory.list",
            lambda *args, **kwargs: [
                inventree.part.PartCategory(
                    test_api, data={"pk": 1, "name": "Resistors", "parent": None}
                )
            ],
        )
        monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "0")
        monkeypatch.setattr("inventree.part.Part.list", lambda *args, **kwargs: [])
        monkeypatch.setattr(
            inventree.part.Part, "uploadImage", lambda *args, **kwargs: None
        )
        monkeypatch.setattr(inventree.part.Part, "create", mock_create_part)
        monkeypatch.setattr(
            "digikey.product_details",
            lambda x: test_data["test_api_responses"][f"{supplier}_resp"],
        )

        test_part = test_module.InventreePart(supplier_part_number, supplier)
        test_part.import_part_from_supplier(test_data["config_reader"])
        test_inv_part = test_part.create_inventree_part(test_data["config_reader"])

        assert test_inv_part.pk == 1
        assert test_inv_part.name == mfg_part_number
        assert test_inv_part.category == 1

    def test_create_inventree_part_exists(
        self,
        supplier_part_number,
        supplier,
        supplier_wrapper_class,
        mfg_part_number,
        mfg,
        monkeypatch,
        test_data,
    ):
        monkeypatch.setattr(
            test_module,
            "find_category",
            lambda *args, **kwargs: inventree.part.PartCategory(
                test_api, data={"pk": 1}
            ),
        )
        monkeypatch.setattr(
            inventree.part.Part, "uploadImage", lambda *args, **kwargs: None
        )
        monkeypatch.setattr(inventree.part.Part, "create", mock_create_part)
        monkeypatch.setattr(
            inventree.part.Part,
            "list",
            lambda *args, **kwargs: [
                inventree.part.Part(
                    test_api,
                    data={
                        "pk": 1,
                        "name": mfg_part_number,
                        "description": supplier_part_number,
                    },
                )
            ],
        )
        monkeypatch.setattr(
            "digikey.product_details",
            lambda x: test_data["test_api_responses"][f"{supplier}_resp"],
        )

        test_part = test_module.InventreePart(supplier_part_number, supplier)
        test_part.import_part_from_supplier(test_data["config_reader"])
        test_inv_part = test_part.create_inventree_part(test_data["config_reader"])

        assert test_inv_part.pk == 1
        assert test_inv_part.name == mfg_part_number
        assert test_inv_part.description == supplier_part_number

    def test_create_manufacturer_part(
        self,
        supplier_part_number,
        supplier,
        supplier_wrapper_class,
        mfg_part_number,
        mfg,
        monkeypatch,
        test_data,
        test_api,
    ):
        monkeypatch.setattr(
            test_module,
            "find_category",
            lambda *args, **kwargs: inventree.part.PartCategory(
                test_api, data={"pk": 1}
            ),
        )
        monkeypatch.setattr(inventree.part.Part, "create", mock_create_part)
        monkeypatch.setattr("inventree.part.Part.list", lambda *args, **kwargs: [])
        monkeypatch.setattr(
            inventree.part.Part, "uploadImage", lambda *args, **kwargs: None
        )
        monkeypatch.setattr(
            inventree.base.InventreeObject, "reload", lambda *args, **kwargs: None
        )

        monkeypatch.setattr(
            inventree.company.ManufacturerPart,
            "create",
            lambda *args, **kwargs: inventree.company.ManufacturerPart(
                test_api, 1, data=args[1]
            ),
        )
        monkeypatch.setattr(
            "inventree.company.Company.list",
            lambda *args, **kwargs: [
                inventree.company.Company(
                    test_api,
                    data={
                        "pk": 1,
                        "name": supplier,
                        "description": supplier,
                    },
                ),
                inventree.company.Company(
                    test_api,
                    data={
                        "pk": 2,
                        "name": mfg,
                        "description": mfg,
                    },
                ),
            ],
        )
        monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "1")
        monkeypatch.setattr(
            "digikey.product_details",
            lambda x: test_data["test_api_responses"][f"{supplier}_resp"],
        )

        test_part = test_module.InventreePart(supplier_part_number, supplier)
        test_part.import_part_from_supplier(test_data["config_reader"])
        test_inv_part = test_part.create_inventree_part(test_data["config_reader"])
        test_mfg_part = test_part.create_manufacturer_part(
            test_data["config_reader"], test_inv_part.pk
        )

        assert test_mfg_part.MPN == mfg_part_number
        assert test_mfg_part.manufacturer == 2
        assert test_mfg_part.part == test_inv_part.pk

    def test_find_manufacturer_exists(
        self,
        supplier_part_number,
        supplier,
        supplier_wrapper_class,
        mfg_part_number,
        mfg,
        monkeypatch,
        test_data,
        test_api,
    ):
        monkeypatch.setattr(
            inventree.company.Company,
            "list",
            lambda *args, **kwargs: [
                inventree.company.Company(
                    test_api,
                    data={
                        "pk": 1,
                        "name": mfg,
                        "description": mfg,
                        "is_supplier": False,
                    },
                )
            ],
        )
        monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "0")
        test_manufacturer = test_module.find_manufacturer(
            test_data["test_dkpart"], test_data["config_reader"]
        )
        assert test_manufacturer.pk == 1
        assert test_manufacturer.name == mfg
        assert test_manufacturer.is_supplier == False
        assert test_manufacturer.description == mfg
