from digikey import status_salesorder_id
import digikey  # have to use digikey.product_details for monkeypatch testing
import os
from pathlib import Path

from .SupplierBase import SupplierPartBase
from ..ConfigReader import ConfigReader


class DigikeyPart(SupplierPartBase):
    SUPPLIER_NAME = "Digikey"

    def __init__(self, api_resp, injest_api_automatically=True, prompt=False):
        super().__init__(
            api_resp, injest_api_automatically=injest_api_automatically, prompt=prompt
        )

    def injest_api(self, prompt=False):
        self.manufacturer = self.raw_value.manufacturer.value
        self.mfg_part_num = self.raw_value.manufacturer_part_number
        self.description = self.raw_value.product_description
        self.link = self.raw_value.product_url
        self.supplier_part_num = self.raw_value.digi_key_part_number
        self.picture = self.raw_value.primary_photo
        for raw_param in self.raw_value.parameters:
            cleaned_param = (raw_param.parameter, raw_param.value)
            self.parameters.append(cleaned_param)

        self.set_part_name(self.raw_value.manufacturer_part_number, prompt=prompt)

    def _extract_picture(self):
        for media in self.raw_value.media_links:
            print(media.media_type)
            if "Product Photos" in media.media_type:
                self.picture = "%s" % media.url

    @classmethod
    def from_supplier_part_number(
        cls,
        partnum: str,
        config: ConfigReader,
        injest_api_automatically=True,
        prompt=False,
    ) -> "DigikeyPart":
        cls._set_environment(config)
        raw = digikey.product_details(partnum)
        if injest_api_automatically:
            part = cls(raw)
            part.injest_api(prompt=prompt)
            return part
        else:
            return cls(raw)

    @staticmethod
    def _set_environment(config):
        if (
            config.digikey_client_id
            and config.digikey_client_secret
            and config.digikey_client_sandbox
            and config.digikey_storage_path
        ):
            os.environ["DIGIKEY_CLIENT_ID"] = config.digikey_client_id
            os.environ["DIGIKEY_CLIENT_SECRET"] = config.digikey_client_secret
            os.environ["DIGIKEY_CLIENT_SANDBOX"] = config.digikey_client_sandbox
            os.environ["DIGIKEY_STORAGE_PATH"] = config.digikey_storage_path
        else:
            errmsg = "Cannot set environment variables for digikey module. Please set "
            if not config.digikey_client_id:
                errmsg += "DIGIKEY_CLIENT_ID "
            if not config.digikey_client_secret:
                errmsg += "DIGIKEY_CLIENT_SECRET "
            if not config.digikey_client_sandbox:
                errmsg += "DIGIKEY_CLIENT_SANDBOX "
            if not config.digikey_storage_path:
                errmsg += "DIGIKEY_STORAGE_PATH "

            raise AttributeError(errmsg)
