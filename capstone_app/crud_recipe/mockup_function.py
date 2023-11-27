import pint
from simple_test import test
from pint import UnitRegistry
from pint.errors import UndefinedUnitError,DimensionalityError


# processes a list of lists
def recipe_processor(list_of_recipes: list):
    ureg = UnitRegistry()
    ingr_dict = {}
    list_for_dimensionality_error_items = []
    for recipe in list_of_recipes:
        for ingredient in recipe:
            item = ingredient[0]
            quantity = ingredient[1]
            msmt = ingredient[2]
            try:
                quantity_msmt = quantity * ureg(msmt)
                if item in ingr_dict:
                    ingr_dict[item] += quantity_msmt
                else:
                    ingr_dict[item] = quantity_msmt
            except UndefinedUnitError:
                quantity_msmt2 = quantity, msmt
                if item in ingr_dict:
                    ingr_dict[item] += quantity_msmt2
                else:
                    ingr_dict[item] = quantity_msmt2
            except DimensionalityError:
                ingredient_tuple = item, quantity, msmt
                list_for_dimensionality_error_items.append(ingredient_tuple)
                # print(item, quantity, msmt)
            
                # list_for_dimensionality_error_items.append(tuple(item, float(quantity), msmt))

    return ingr_dict, list_for_dimensionality_error_items