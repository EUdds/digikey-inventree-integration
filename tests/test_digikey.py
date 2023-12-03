from inventree_digikey.Digikey import DigiPart
from digikey.v3.api import DigikeyApiWrapper
import digikey

def test_part_creation(test_data):
    test_resp = test_data["test_resp"]
    dkpart = DigiPart(test_resp)
    dkpart.injest_api(prompt=False)
    assert dkpart.manufacturer == "Texas Instruments", "Manufacturer not set correctly: Got %s expected %s" %(dkpart.manufacturer, "Texas Instruments")
    assert dkpart.mfg_part_num == "NA555DR", "MFG Part Number not set correctly"
    assert dkpart.name == "NA555DR", "Name not set correctly"
    assert dkpart.description == "IC OSC SGL TIMER 100KHZ 8-SOIC", "Description not set correctly"
    assert dkpart.link == "https://www.digikey.com/en/products/detail/texas-instruments/NA555DR/1571933"
    assert dkpart.digi_part_num == "296-21752-2-ND"
    assert dkpart.picture == "https://mm.digikey.com/Volume0/opasdata/d220001/medias/images/4849/296_8-SOIC.jpg"
    for param in test_resp.parameters:
        assert (param.parameter, param.value) in dkpart.parameters, "Parameter not set correctly"

def test_part_creation_from_partnumber(test_data, monkeypatch):
    monkeypatch.setattr('digikey.product_details', lambda x: test_data["test_resp"])
    dkpart = DigiPart.from_digikey_part_number("296-21752-2-ND", test_data['config_reader'])
    dkpart.injest_api(prompt=False)
    
    assert dkpart.manufacturer == "Texas Instruments", "Manufacturer not set correctly: Got %s expected %s" %(dkpart.manufacturer, "Texas Instruments")
    assert dkpart.mfg_part_num == "NA555DR", "MFG Part Number not set correctly"
    assert dkpart.name == "NA555DR", "Name not set correctly"
    assert dkpart.description == "IC OSC SGL TIMER 100KHZ 8-SOIC", "Description not set correctly"
    assert dkpart.link == "https://www.digikey.com/en/products/detail/texas-instruments/NA555DR/1571933"
    assert dkpart.digi_part_num == "296-21752-2-ND"
    assert dkpart.picture == "https://mm.digikey.com/Volume0/opasdata/d220001/medias/images/4849/296_8-SOIC.jpg"
    for param in test_data['test_resp'].parameters:
        assert (param.parameter, param.value) in dkpart.parameters, "Parameter not set correctly"
