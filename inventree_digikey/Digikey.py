from digikey import product_details


def get_part_from_part_number(partnum: str):
    raw = product_details(partnum)
    part = DigiPart(raw)
    part.injest_api()
    return part

class DigiPart:
    def __init__(self, api_value):
        self.part = None
        self.supplier = "Digikey"
        self.digi_part_num = None
        self.mfg_part_num = None
        self.manufacturer = None
        self.description = None
        self.link = None
        self.price_breaks = []
        self.raw_value = api_value
        self.parameters = []


    def injest_api(self):
        self.manufacturer = self.raw_value.manufacturer.value
        self.mfg_part_num = self.raw_value.manufacturer_part_number
        self.description = self.raw_value.product_description
        self.link = self.raw_value.product_url
        self.digi_part_num = self.raw_value.digi_key_part_number

        for raw_param in self.raw_value.parameters:
            cleaned_param = (raw_param.parameter, raw_param.value)
            self.parameters.append(cleaned_param)


    def set_part_name(self, name: str):
        self.part = name
