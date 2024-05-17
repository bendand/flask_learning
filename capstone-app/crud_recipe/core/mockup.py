import pint
# from simple_test import test
from pint import UnitRegistry
from pint.errors import UndefinedUnitError

ureg = UnitRegistry()


# - take several recipes, with multiple ingredients
# - combine those recipes into a single list of ingredients to use as a shopping list
# - use pint to add similar units of measure together
# - Keep an eye out for weight vs volume measures, and make sure you test that you've accounted for the difference
# * 		recipe1 = [
# * 		  ("rice", 1, "cup"),
# * 		  ("salt", 1, "tsp")
# * 		]


# print(height)


def add_ingredients(recipe):
    ureg = UnitRegistry()
    ingr_dict = {}
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

    return ingr_dict


some_recipe = [("rice", 1, "cup"), ("salt", 1, "tsp"),
               ("rice", 1/4, "cup"), ("garlic cloves", 2, "count"), ("salt", 5, "tbsp"), ("garlic cloves", 2, "count")]



print(add_ingredients(
    [("rice", 1, "cup"),
     ("salt", 1, "tsp"),
     ("rice", 1/4, "cup"), ("garlic cloves", 2, "count"), ("salt", 5, "tbsp"), ("garlic cloves", 2, "count")]) == {'rice': 1.25 * ureg('cup'), 'salt': 16.0 * ureg('teaspoon'), 'garlic cloves': 4 * ureg('count')})
