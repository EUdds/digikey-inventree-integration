import inventree_digikey_integration.__main__ as test_module
import inventree_digikey_integration.Inventree

from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parent.parent / "inventree_digikey_integration"


def test_argparse():
    args = test_module.parse_args(["-y", "1234", "5678"])
    assert args.yes == True
    assert args.query_numbers == ["1234", "5678"]
    assert args.config == test_module.DEFAULT_CONFIG_PATH

    args = test_module.parse_args(["-y", "1234", "5678"])
    assert args.yes == True
    assert args.query_numbers == ["1234", "5678"]
    assert args.config == test_module.DEFAULT_CONFIG_PATH

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


def test_import_parts(monkeypatch, test_data):
    monkeypatch.setattr(
        inventree_digikey_integration.Inventree.InventreePart,
        "import_part_from_supplier",
        lambda *args: None,
    )
    monkeypatch.setattr(
        inventree_digikey_integration.Inventree.InventreePart,
        "add_to_inventree",
        lambda *args: None,
    )

    # Format (args, expected_return)
    test_inputs = [
        (["-c", f"{test_data['test_config_path']}", "4116R-1-151LF"], 1),
    ]
    for test_input in test_inputs:
        args = test_module.parse_args(test_input[0])
        res = test_module.import_parts(args)
        assert (
            res == test_input[1]
        ), "Expected return value of {} is {} but got {}".format(
            test_input[0], test_input[1], res
        )
