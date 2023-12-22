import argparse
import sys

from .Inventree import import_digikey_part
from .ConfigReader import ConfigReader
from pathlib import Path

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "config.ini"


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Import Digikey part numbers into InvenTree"
    )

    # Add an optional '-y' flag to bypass prompting
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help='Bypass user prompts and assume "yes"',
        default=False,
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        help="Path to config file",
        default=DEFAULT_CONFIG_PATH,
    )

    # Add the 'part_number' argument as the last item on the command line
    parser.add_argument(
        "query_numbers", type=str, help="Part number(s) to import", nargs="*"
    )

    return parser.parse_args(args)


def import_parts(args):
    config = ConfigReader(args.config)
    if len(args.query_numbers) == 0:
        partnum = input("Enter a digikey Part Number > ")
        import_digikey_part(partnum, config, not args.yes)
        return 1
    else:
        for num in args.query_numbers:
            import_digikey_part(num, config, not args.yes)
        return len(args.query_numbers)


def main():
    args = parse_args(sys.argv[1:])
    num_parts = import_parts(args)
    print(f"Attempted to import {num_parts} parts")


if __name__ == "__main__":
    main()
