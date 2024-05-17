import pint
from pint import UnitRegistry, Quantity

ingredient_name_dict = {}


recipe_items = [('oregano', '2', 'tablespoons'), ('parsley', '3', 'teaspoons'), ('ground beef', '2', 'pounds'), ('parsley', '2', 'tbsp')]

ureg = UnitRegistry()
ingr_dict = {}

for ingredient in recipe_items:
    item = ingredient[0]
    quantity = int(ingredient[1])
    msmt = ingredient[2]

    quantity_msmt = quantity * ureg(msmt)
    if item in ingr_dict:
        ingr_dict[item] += quantity_msmt
    else:
        ingr_dict[item] = quantity_msmt


for item in ingr_dict.items():
    print(item)
    

distilled_ingredients = [(item, quantity) for item, quantity in ingr_dict.items()]


for data_tuple in distilled_ingredients:
    item, quantity, measurement = data_tuple

    amount = quantity.magnitude




    



    




def recipe_processor(list_of_recipes: list):
    ureg = UnitRegistry()
    ingr_dict = {}
    for recipe in list_of_recipes:
        for ingredient in recipe:
            item = ingredient[0]
            quantity = ingredient[1]
            msmt = ingredient[2]
    
            quantity_msmt = quantity * ureg(msmt)
            if item in ingr_dict:
                ingr_dict[item] += quantity_msmt
            else:
                ingr_dict[item] = quantity_msmt

    return ingr_dict




