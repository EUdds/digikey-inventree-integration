import inventree_digikey.__main__ as test_module

from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parent.parent / "inventree_digikey"


def test_argparse():
    args = test_module.parse_args(["-y", "1234", "5678"])
    assert args.yes == True
    assert args.query_numbers == ["1234", "5678"]
    assert args.config == SOURCE_ROOT / "config.ini"

    args = test_module.parse_args(["-y", "1234", "5678"])
    assert args.yes == True
    assert args.query_numbers == ["1234", "5678"]
    assert args.config == SOURCE_ROOT / "config.ini"

    args = test_module.parse_args(["-y", "-c", "test_config.ini", "1234", "5678"])
    assert args.yes == True
    assert args.query_numbers == ["1234", "5678"]
    assert args.config == Path("test_config.ini")

    args = test_module.parse_args(["-y", "-c", "test_config.ini", "1234", "5678"])
    assert args.yes == True
    assert args.query_numbers == ["1234", "5678"]
    assert args.config == Path("test_config.ini")

    args = test_module.parse_args(["-y", "-c", "test_config.ini", "1234", "5678"])
    assert args.yes == True
    assert args.query_numbers == ["1234", "5678"]
    assert args.config == Path("test_config.ini")

    args = test_module.parse_args(["-y", "-c", "test_config.ini", "1234", "5678"])
    assert args.yes == True
    assert args.query_numbers == ["1234", "5678"]
    assert args.config == Path("test_config.ini")

    args = test_module.parse_args(["-y", "-c", "test_config.ini", "1234", "5678"])
    assert args.yes == True
    assert args.query_numbers == ["1234", "5678"]
    assert args.config == Path("test_config.ini")

    args = test_module.parse_args(["-y", "-c", "test_config.ini", "1234", "5678"])
    assert args.yes == True
    assert args.query_numbers == ["1234", "5678"]
    assert args.config == Path("test_config.ini")
