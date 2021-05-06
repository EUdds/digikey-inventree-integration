from digikey import product_details

from .ImageManager import ImageManager


def get_part_from_part_number(partnum: str):
    raw = product_details(partnum)
    print(raw)
    part = DigiPart(raw)
    part.injest_api()
    return part

class DigiPart:
    def __init__(self, api_value):
        self.name = None
        self.supplier = "Digikey"
        self.digi_part_num = None
        self.mfg_part_num = None
        self.manufacturer = None
        self.description = None
        self.link = None
        self.price_breaks = []
        self.raw_value = api_value
        self.parameters = []
        self.picture = None
        self.thumbnail = None


    def injest_api(self):
        self.manufacturer = self.raw_value.manufacturer.value
        self.mfg_part_num = self.raw_value.manufacturer_part_number
        self.description = self.raw_value.product_description
        self.link = self.raw_value.product_url
        self.digi_part_num = self.raw_value.digi_key_part_number
        self.picture = self.raw_value.primary_photo
        for raw_param in self.raw_value.parameters:
            cleaned_param = (raw_param.parameter, raw_param.value)
            self.parameters.append(cleaned_param)

        self.prompt_part_name()


    def set_part_name(self, name: str):
        self.name = name

    def prompt_part_name(self):
        found_name = self.raw_value.manufacturer_part_number
        print(f"Found {found_name} - Would you like to use this name (y/n)")
        ans = input("> ")
        if ans == "y":
            self.set_part_name(found_name)
        else:
            print("Type a new name")
            name = input("> ")
            self.set_part_name(name)


    def _extract_picture(self):
        for media in self.raw_value.media_links:
            print(media.media_type)
            if "Product Photos" in media.media_type:
                self.picture = "%s" % media.url

