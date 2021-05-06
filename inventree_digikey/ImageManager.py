import os
import requests
import random
import string

from pathlib import Path

class ImageManager:

    cache_path: Path = Path(__file__).resolve().parent / "cache"

    @classmethod
    def get_image(cls, url:str) -> str:
        """
        Gets an image given an url
        returns a filepath
        """
        if not cls.cache_active():
            print("Cache not active creating...")
            cls._create_cache()

        path = cls._download_image(url)
        return path

    @classmethod
    def cache_active(cls):
        print(os.path.exists(cls.cache_path))
        return os.path.exists(cls.cache_path)

    @classmethod
    def _create_cache(cls):
        try:
            print(f"Making cache at {cls.cache_path}")
            os.mkdir(cls.cache_path)
        except:
            print("Error making cache")

    @classmethod
    def clean_cache(cls):
        if cls.cache_active:
            for f in Path(cls.cache_path).glob("*"):
                f.unlink()

    def _filename_generator(size=6) -> str:
        return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))

    @classmethod
    def _download_image(cls, url:str) -> str:
        print(f"Trying URL {url}")
        res = requests.get(url, stream=True)

        if not res.ok:
            print(f"ERROR: Request code is {res.status_code}")
            return -1

        filename = cls._filename_generator()

        filepath = cls.cache_path / filename
        with open(filepath, 'wb') as handler:
            for block in res.iter_content(1024):
                if not block:
                    break
                handler.write(block)

        return filepath

