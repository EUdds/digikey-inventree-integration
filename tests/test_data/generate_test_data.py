from digikey import product_details
import pickle
from pathlib import Path
import os

os.sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from inventree_digikey_integration.suppliers.Digikey import DigikeyPart


TEST_DATA_PATH = Path(__file__).resolve().parent

APIS_TO_TEST = [
    # Name,     Supplier Wrapper,   API Request Function,   Part Number under test
    ["Digikey", DigikeyPart, product_details, "296-21752-2-ND"],
]

for APIS_TO_TEST in APIS_TO_TEST:
    print("Fetching test data from %s API" % APIS_TO_TEST[0])
    resp = APIS_TO_TEST[2](APIS_TO_TEST[3])
    dump_path = (
        TEST_DATA_PATH / "supplier_api_responses" / (APIS_TO_TEST[0] + "_resp.pkl")
    )
    print("Saving test data to %s" % str(dump_path))
    with open(dump_path, "wb") as f:
        pickle.dump(resp, f)


print("Saving test data to %s" % str(Path(TEST_DATA_PATH) / "test_dkpart.pkl"))
with open(TEST_DATA_PATH / "test_dkpart.pkl", "wb") as f:
    dkpart = DigikeyPart(resp)
    dkpart.injest_api(prompt=False)
    pickle.dump(dkpart, f)

print("Test data saved")
