from inventree_digikey.ImageManager import ImageManager
import random
import pytest

from pathlib import Path

@pytest.fixture()
def tempdir(tmpdir_factory):
    return Path(tmpdir_factory.mktemp("cache"))


def test_image_manager_cache_path(tempdir):
    ImageManager.cache_path = tempdir / f"{random.randint(0, 100000)}"
    ImageManager._create_cache()
    assert Path(ImageManager.cache_path).exists()


def test_image_manager_get_image(tempdir, test_data):
    ImageManager.cache_path = tempdir 
    path = ImageManager.get_image(test_data["test_image"]["url"])
    assert Path(path).exists()
    assert Path(path).stat().st_size <= test_data["test_image"]["size"] * (1 + test_data["test_image"]["size_error"])
    assert Path(path).stat().st_size >= test_data["test_image"]["size"] * (1 - test_data["test_image"]["size_error"])
    assert Path(path).suffix == ".jpg"
