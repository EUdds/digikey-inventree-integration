import pytest
import inventree_digikey.Inventree as test_module
from configparser import ConfigParser
import inventree.company
import inventree.api


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
    monkeypatch.setattr(inventree.api.InvenTreeAPI, 'connect', lambda *args, **kwargs: None)
    api =  inventree.api.InvenTreeAPI(test_data['test_config']['INVENTREE_API']['URL'], username=test_data['test_config']['INVENTREE_API']['USER'], password=test_data['test_config']['INVENTREE_API']['PASSWORD'])
    return api
    # Cleanup here as necessary

def test_get_digikey_supplier_new_company(test_api, monkeypatch, test_supplier_data):
    monkeypatch.setattr(inventree.company.Company, 'list', lambda *args, **kwargs: [])
    monkeypatch.setattr(inventree.company.Company, 'create', mock_create_company)
    dk = test_module.get_digikey_supplier()
    assert dk.pk == 1
    assert dk.name == "Digikey"
    assert dk.is_supplier == True
    assert dk.description == "Electronics Supply Store"


def test_get_digikey_supplier_existing_company(test_api, test_supplier_data, monkeypatch):
    monkeypatch.setattr(inventree.company.Company, 'list', lambda *args, **kwargs: [inventree.company.Company(test_api, data=test_supplier_data)]) 
    dk = test_module.get_digikey_supplier()
    assert dk.pk == 1



def test_create_inventree_part(monkeypatch, test_data, test_api):
    monkeypatch.setattr(test_module, 'find_category', lambda *args, **kwargs: inventree.part.PartCategory(test_api, data={"pk": 1}))
    monkeypatch.setattr(inventree.part.Part, 'uploadImage', lambda *args, **kwargs: None)
    monkeypatch.setattr(inventree.part.Part, 'create', mock_create_part)
    monkeypatch.setattr(inventree.part.Part, 'list', lambda *args, **kwargs: [])

    inventree_part = test_module.create_inventree_part(test_data["test_dkpart"])
    assert inventree_part.pk == 1
    assert inventree_part.name == test_data["test_dkpart"].name
    assert inventree_part.description == test_data["test_dkpart"].description
    

def test_create_inventree_part_part_exists(test_data, monkeypatch, test_api):
    monkeypatch.setattr(test_module, 'find_category', lambda *args, **kwargs: inventree.part.PartCategory(test_api, data={"pk": 1}))
    monkeypatch.setattr(inventree.part.Part, 'uploadImage', lambda *args, **kwargs: None)
    monkeypatch.setattr(inventree.part.Part, 'create', mock_create_part)
    monkeypatch.setattr(inventree.part.Part, 'list', lambda *args, **kwargs: [inventree.part.Part(test_api, data={"pk": 1, "name": test_data["test_dkpart"].name, "description": test_data["test_dkpart"].description})])

    inventree_part = test_module.create_inventree_part(test_data["test_dkpart"])
    assert inventree_part == -1


def test_find_manufacturer(test_data, monkeypatch, test_api):
    monkeypatch.setattr(inventree.company.Company, 'list', lambda *args, **kwargs: [])
    monkeypatch.setattr(inventree.company.Company, 'create', mock_create_company)
    test_manufacturer = test_module.find_manufacturer(test_data["test_dkpart"])
    assert test_manufacturer.pk == 1
    assert test_manufacturer.name == test_data["test_dkpart"].manufacturer
    assert test_manufacturer.is_supplier == False
    assert test_manufacturer.description == test_data["test_dkpart"].manufacturer

def test_find_manufacturer_manufactuer_exists(test_data, monkeypatch, test_api):
    monkeypatch.setattr(inventree.company.Company, 'list', lambda *args, **kwargs: [inventree.company.Company(test_api, data={"pk": 1, "name": test_data["test_dkpart"].manufacturer, "description": test_data["test_dkpart"].manufacturer, "is_supplier": False})])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: "0")
    test_manufacturer = test_module.find_manufacturer(test_data["test_dkpart"])
    assert test_manufacturer.pk == 1
    assert test_manufacturer.name == "Texas Instruments"
    assert test_manufacturer.is_supplier == False
    assert test_manufacturer.description == "Texas Instruments"

def test_add_digikey_part(test_data, monkeypatch, test_api):
    monkeypatch.setattr(inventree.company.Company, 'list', lambda *args, **kwargs: [inventree.company.Company(test_api, data={"pk": 1, "name": "Digikey", "description": "Electronics Supply Store", "is_supplier": True})])
    monkeypatch.setattr(inventree.part.Part, 'create', mock_create_part)
    monkeypatch.setattr(inventree.part.Part, 'list', lambda *args, **kwargs: [])
    monkeypatch.setattr(inventree.part.Part, 'uploadImage', lambda *args, **kwargs: None)
    monkeypatch.setattr(inventree.part.PartCategory, 'list', lambda *args, **kwargs: [inventree.part.PartCategory(test_api, data={"pk": 1, "name": "Resistors", "parent": None})])
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: "0")
    monkeypatch.setattr(inventree.company.ManufacturerPart, 'create', lambda *args, **kwargs: None)
    monkeypatch.setattr(inventree.company.SupplierPart, 'create', lambda *args, **kwargs: None)

    test_module.add_digikey_part(test_data["test_dkpart"]) # Yeah, I should add some return value error checking type stuff here




