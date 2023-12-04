import argparse
import sys

from .Inventree import import_digikey_part
from pathlib import Path

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "config.ini"


def parse_args(args):
    parser = argparse.ArgumentParser(description='Import Digikey part numbers into InvenTree')

    # Add an optional '-y' flag to bypass prompting
    parser.add_argument('-y', "--yes", action='store_true', help='Bypass user prompts and assume "yes"', default=False)
    parser.add_argument("-c", "--config", type=Path, help="Path to config file", default=DEFAULT_CONFIG_PATH)

    # Add the 'part_number' argument as the last item on the command line
    parser.add_argument('query_numbers', type=str, help='Part number(s) to import', nargs='+')

    return parser.parse_args(args)

def main():
    args = parse_args(sys.argv[1:])
    if len(args.query_numbers) == 0:
        print("No part numbers specified")
        sys.exit(1)
    if len(args.query_number) == 1:
        partnum = input("Enter a digikey Part Number > ")
        import_digikey_part(partnum, not args.yes)
    else:
        for num in args.query_number:
            import_digikey_part(num, not args.yes)

if __name__ == "__main__":
    main()
