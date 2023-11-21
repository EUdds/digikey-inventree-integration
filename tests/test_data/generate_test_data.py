from digikey import product_details
import pickle
from pathlib import Path
import os

os.sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from inventree_digikey.Digikey import DigiPart


TEST_DATA_PATH = Path(__file__).resolve().parent

DIGIKEY_PART_NUMBER_UNDER_TEST ="296-21752-2-ND"

print("Fetching test data from Digikey API")
resp = product_details(DIGIKEY_PART_NUMBER_UNDER_TEST)

print("Saving test data to %s" % str(Path(TEST_DATA_PATH) / "test_resp.pkl"))
with open(TEST_DATA_PATH / "test_resp.pkl", "wb") as f:
    pickle.dump(resp, f)

print("Saving test data to %s" % str(Path(TEST_DATA_PATH) / "test_dkpart.pkl"))
with open(TEST_DATA_PATH / "test_dkpart.pkl", "wb") as f:
    dkpart = DigiPart(resp)
    dkpart.injest_api(prompt=False)
    pickle.dump(dkpart, f)

print("Test data saved")