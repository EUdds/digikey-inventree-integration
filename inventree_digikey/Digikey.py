from digikey import product_details


def get_part_from_part_number(partnum: str):
    return product_details(partnum)
