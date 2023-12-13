import os
import random
import string
import http.client
from urllib.parse import urlparse, quote

from pathlib import Path


class ImageManager:
    cache_path: Path = Path(__file__).resolve().parent / "cache"

    @classmethod
    def get_image(cls, url: str) -> str:
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
        return (
            "".join(
                random.choice(string.ascii_lowercase + string.digits)
                for _ in range(size)
            )
            + ".jpg"
        )

    @classmethod
    def _download_image(cls, url: str) -> str:
        print(f"Trying URL {url}")

        escaped_url = quote(url, safe=":/")

        parsed_url = urlparse(escaped_url)

        # Extract protocol, server host, and path
        protocol = parsed_url.scheme
        server_host = parsed_url.netloc
        path = parsed_url.path

        # Create an HTTP connection to the server based on the protocol
        if protocol == "http":
            conn = http.client.HTTPConnection(server_host)
        elif protocol == "https":
            conn = http.client.HTTPSConnection(server_host)
        else:
            print("Unsupported protocol:", protocol)
            exit(1)

        # Send an HTTP GET request with custom headers
        conn.request("GET", path)

        # Get the response
        response = conn.getresponse()

        if not response.status == 200:
            print(f"ERROR: Request code is {response.status}")
            return -1

        filename = cls._filename_generator()

        filepath = cls.cache_path / filename
        with open(filepath, "wb") as handler:
            while True:
                chunk = response.read(1024)
                if not chunk:
                    break
                handler.write(chunk)

        return str(filepath)
