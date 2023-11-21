from pathlib import Path
from configparser import ConfigParser
import pytest
import pickle

TEST_DATA_PATH = Path(__file__).resolve().parent / "test_data"

@pytest.fixture(scope="session")
def test_data():
    data_dict = {}
    for file in TEST_DATA_PATH.glob("*.pkl"):
        with open(file, "rb") as f:
            data_dict[file.stem] = pickle.load(f)
    for file in TEST_DATA_PATH.glob("*.ini"):
        config = ConfigParser()
        config.read(file)
        data_dict[file.stem] = config
    
    data_dict["test_image"] =  {
        "url":"https://postimg.cc/WF5g5BGP",
        "size": 11688,
        "size_error": 0.1,
    }

    return data_dict

@pytest.fixture
def test_supplier_data():
    return {
        "name": "Digikey",
        "is_supplier": True,
        "description": "Electronics Supply Store",
        "pk": 1
    }