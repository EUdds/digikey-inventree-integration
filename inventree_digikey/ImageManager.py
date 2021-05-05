import os
import requests
import random
import string

from pathlib import Path

class ImageManager:

    cache_path: Path = Path(__file__).resolve().parent

    @classmethod
    def get_image(cls, url:str) -> str:
        """
        Gets an image given an url
        returns a filepath
        """
        if not cls.cache_active:
            cls._create_cache()

        path = cls._download_image(url)
        return path


    @property
    def cache_active(cls):
        return os.path.isdir(cls.cache_path)

    def _create_cache():
        try:
            os.mkdir(cache_path)
        except:
            print("Error making cache")

    def _clean_cache(cls):
        if cls.cache_active:
            os.rmdir(cache_path)

    def _filename_generator(size=6) -> str:
        return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))

    @classmethod
    def _download_image(cls, url:str) -> str:
        res = requests.get(url, stream=True)

        if not res.ok:
            return -1

        filename = cls._filename_generator()

        filepath = cls.cache_path / filename
        with open(filepath, 'wb') as handler:
            for block in res.iter_content(1024):
                if not block:
                    break
                handler.write(block)

        return filepath

