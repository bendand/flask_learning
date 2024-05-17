import pint
from simple_test import test
from pint import UnitRegistry
from pint.errors import UndefinedUnitError,DimensionalityError


def recipe_reducer(list_of_ingredients):
    ureg = UnitRegistry()
    ingredient_dict = {}
    
    for ingredient in list_of_ingredients:
        ingredient_name = ingredient[0]
        ingredient_quantity = ingredient[1]
        ingredient_msmt = ingredient[2]
        quantity_msmt = ingredient_quantity * ureg(ingredient_msmt)

        if quantity_msmt.check('[volume]') == True:
            dimension = 'volume'
        elif quantity_msmt.check('[mass]') == True:
            dimension = 'mass'
        else: 
            dimension = 'other'

        name_and_dimension = (ingredient_name, dimension)
        
        if name_and_dimension in ingredient_dict:
            ingredient_dict[name_and_dimension] += quantity_msmt
        else:
            ingredient_dict[name_and_dimension] = quantity_msmt
    
    final_ingredient_list = []

    for ingredient, measurement in ingredient_dict.items():
        new_tuple = (ingredient[0], float(measurement.magnitude), str(measurement.units))
        final_ingredient_list.append(new_tuple)

    return final_ingredient_list

    

