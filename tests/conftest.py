from pathlib import Path
from configparser import ConfigParser
import pytest
import pickle
import os

from inventree_digikey_integration.ConfigReader import ConfigReader

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
        data_dict[f"{file.stem}_path"] = file

    data_dict["config_reader"] = ConfigReader(TEST_DATA_PATH / "test_config.ini")

    data_dict["test_image"] = {
        "url": "https://postimg.cc/WF5g5BGP",
        "size": 11688,
        "size_error": 0.2,  # Add some error margin for different download sizes
    }

    return data_dict


@pytest.fixture
def test_supplier_data():
    return {
        "name": "Digikey",
        "is_supplier": True,
        "description": "Electronics Supply Store",
        "pk": 1,
    }

