from inventree_digikey_integration.ConfigReader import ConfigReader

class SupplierPartBase:

    SUPPLIER_NAME = None

    def __init__(self, api_resp, injest_api_automatically=True, prompt=False):
        self.raw_value = api_resp
        self.name = None
        self.supplier_part_num = None
        self.mfg_part_num = None
        self.manufacturer = None
        self.description = None
        self.link = None
        self.price_breaks = []
        self.parameters = []
        self.picture = None
        self.thumbnail = None
        self.supplier = self.SUPPLIER_NAME

        if injest_api_automatically:
            self.injest_api()
    
    def injest_api(self, prompt=False):
        raise NotImplementedError("SupplierPartBase.injest_api not implemented, use a specific supplier subclass")

    def set_part_name(self, manufacturer_part_number: str, prompt=False):
        if not prompt:
            self.name = manufacturer_part_number
            return
        print(f"Found {manufacturer_part_number} - Would you like to use this name (y/n)")
        ans = input("> ").strip().lower()
        while ans not in ["y", "n"]:
            print("Invalid input, try again")
            ans = input("> ").strip().lower()
        if ans == "y":
            self.name = manufacturer_part_number
        else:
            print("Enter a new name")
            name = input("> ").strip()
            self.name = name
    
    def _extract_picture(self):
        raise NotImplementedError("SupplierPartBase._extract_picture not implemented, use a specific supplier subclass")

    @classmethod
    def from_supplier_part_number(cls, partnum: str, config: ConfigReader, injest_api_automatically=True, prompt=False):
        raise NotImplementedError("SupplierPartBase.from_supplier_part_number not implemented, use a specific supplier subclass")