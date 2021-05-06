import os
import digikey
import configparser

from .Digikey import get_part_from_part_number
from pathlib import Path
from digikey.v3.productinformation import KeywordSearchRequest
from .Inventree import add_digikey_part

config = configparser.ConfigParser()
config_path = Path(__file__).resolve().parent / 'config.ini'
config.read(config_path)

os.environ['DIGIKEY_CLIENT_ID'] = config['DIGIKEY_API']['CLIENT_ID']
os.environ['DIGIKEY_CLIENT_SECRET'] = config['DIGIKEY_API']['CLIENT_SECRET']
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = '.'


partnum = input("Enter a digikey partnum > ")

dkpart = get_part_from_part_number(partnum)
print(dkpart)

add_digikey_part(dkpart)
