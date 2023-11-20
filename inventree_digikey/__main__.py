from . import import_digikey_part, import_digikey_order
import sys
import argparse

parser = argparse.ArgumentParser(description='Import Digikey part numbers into InvenTree')

# Add an optional '-y' flag to bypass prompting
parser.add_argument('-y', action='store_true', help='Bypass user prompts and assume "yes"')
parser.add_argument('-o', action='store_true', help='Query and Order number and import it')

# Add the 'part_number' argument as the last item on the command line
parser.add_argument('part_number', type=str, help='Part number to import')

args = parser.parse_args()
if args.o:
    if len(sys.argv) > 1:
        ordernum = args.part_number
    else:
        ordernum = input("Enter a Digikey Order Number > ")

    import_digikey_order(ordernum)
else:
    if len(sys.argv) > 1:
        partnum = args.part_number
    else:
        partnum = input("Enter a digikey Part Number > ")

    import_digikey_part(partnum, not args.y)
