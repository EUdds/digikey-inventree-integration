import pytest

from inventree_digikey_integration.suppliers import DigikeyPart

CLASSES_UNDER_TEST = [
    DigikeyPart,
]

REQUIRED_FIELDS = [
    "mfg_part_num",
    "supplier_part_num",
    "description",
    "link",
    "name",
]

@pytest.mark.parametrize('class_under_test', CLASSES_UNDER_TEST)
class TestSupplierPart:
    def test_has_required_fields(self, class_under_test, test_data):
        resp = test_data["test_api_responses"][class_under_test.__name__]
        part = class_under_test(resp, injest_api_automatically=False)
        for field in REQUIRED_FIELDS:
            assert hasattr(part, field), f"Instance of class {class_under_test} is missing required field {field}"
    
    def test_filled_required_fields(self, class_under_test, test_data):
        test_resp = test_data["test_api_responses"][class_under_test.__name__]
        dkpart = class_under_test(test_resp)
        dkpart.injest_api(prompt=False)
        for field in REQUIRED_FIELDS:
            assert getattr(dkpart, field), f"Class {class_under_test} is missing required field {field}"


