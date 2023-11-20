from .Digikey import get_order_from_order_number
from .Inventree import import_digikey_part, add_digikey_order

def import_digikey_order(order_number: str):
    dkorder = get_order_from_order_number(order_number)
    print(dkorder.order_number)
    for line_item in dkorder.line_items:
        print(line_item.digi_key_part_number)
    return add_digikey_order(dkorder)