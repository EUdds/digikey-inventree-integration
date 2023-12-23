import configparser

from pathlib import Path
from inventree.api import InvenTreeAPI


class ConfigReader:
    """
    Manage global configuration settings and Inventree instance

    Optionally read configuration from a file
    """

    DEFAULT_DIGIKEY_STORAGE_PATH = "."
    DEFAULT_DIGIKEY_CLIENT_SANDBOX = "False"

    def __init__(self, config_file=None):
        self.config = configparser.ConfigParser()

        self.digikey_client_id = None
        self.digikey_client_secret = None
        self.digikey_client_sandbox = self.DEFAULT_DIGIKEY_CLIENT_SANDBOX
        self.digikey_storage_path = self.DEFAULT_DIGIKEY_STORAGE_PATH

        self.inventree_url = None
        self.inventree_username = None
        self.inventree_password = None
        self._inventree_api = None
        self._reinit_api = False

        if config_file:
            self.read_config(config_file)

    def read_config(self, config_file: Path) -> None:
        """
        Read configuration from a file
        """
        self.config.read(config_file)
        self.digikey_client_id = self.config["DIGIKEY_API"]["CLIENT_ID"]
        self.digikey_client_secret = self.config["DIGIKEY_API"]["CLIENT_SECRET"]
        if "SANDBOX" in self.config["DIGIKEY_API"]:
            self.digikey_client_sandbox = self.config["DIGIKEY_API"].getboolean(
                "SANDBOX"
            )
        if "STORAGE_PATH" in self.config["DIGIKEY_API"]:
            self.digikey_storage_path = self.config["DIGIKEY_API"]["STORAGE_PATH"]
        self._inventree_url = self.config["INVENTREE_API"]["URL"]
        self._inventree_username = self.config["INVENTREE_API"]["USER"]
        self._inventree_password = self.config["INVENTREE_API"]["PASSWORD"]

    @property
    def inventree_api(self):
        if (
            self._inventree_api is None or self._reinit_api
        ):  # Allows us to reinit the api if the config changes
            if (
                self.inventree_url
                and self.inventree_username
                and self.inventree_password
            ):
                try:
                    api = InvenTreeAPI(
                        self.inventree_url,
                        username=self.inventree_username,
                        password=self.inventree_password,
                    )
                except:
                    print("Error: Could not connect to Inventree API")  # FIXME
                    return None

                self._reinit_api = False
                self._inventree_api = api
                return api
            else:
                raise AttributeError(
                    "Cannot init inventree_api without inventree_[url|username|password] set"
                )
        else:
            return self._inventree_api

    @inventree_api.setter
    def inventree_api(self, value):
        raise AttributeError(
            "Cannot set inventree_api directly. Use inventree_[url|username|password] instead"
        )

    @property
    def inventree_url(self):
        return self._inventree_url

    @property
    def inventree_username(self):
        return self._inventree_username

    @property
    def inventree_password(self):
        return self._inventree_password

    @inventree_url.setter
    def inventree_url(self, value):
        self._reinit_api = True
        self._inventree_url = value

    @inventree_username.setter
    def inventree_username(self, value):
        self._reinit_api = True
        self._inventree_username = value

    @inventree_password.setter
    def inventree_password(self, value):
        self._reinit_api = True
        self._inventree_password = value
