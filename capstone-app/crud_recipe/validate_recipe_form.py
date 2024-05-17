from pint import UnitRegistry
from crud_recipe.recipes.forms import RecipeForm
from flask import render_template,redirect,url_for


class ValidationError(Exception):

    message = "your data is invalid"

    def __init__(self, errors):            
        self.errors = errors




def validate_add_recipe_form(recipe_data):
    # initialize our validation error message dictionary
    errors = {}
    # repository for clean ingredients
    clean_ingredients = {}

    for line_num, line in enumerate(recipe_data):
        
        raw_ingredient = line.split(', ')
        # print(raw_ingredient)
        if len(raw_ingredient) != 3:
            if "tuple length" in errors:
                errors["tuple length"] += ', ' +  str(line_num + 1)
            else:
                errors["tuple length"] = str(line_num + 1)
            continue

        name = raw_ingredient[0].strip() 
        quantity = raw_ingredient[1].strip() 
        measure = raw_ingredient[2].strip()
        ureg = UnitRegistry()

        # initializes our validation error to False
        validation_error = False

        try:
            quantity_float = float(quantity)
        except:
            validation_error = True
            if "quantity value" in errors:
                errors["quantity value"] += ', ' + str(line_num + 1)
            else:
                errors["quantity value"] = str(line_num + 1)

        try:
            ureg(measure)
        except:
            validation_error = True
            if "invalid measurement" in errors:
                errors["invalid measurement"] += ', ' + str(line_num + 1)
            else:
                errors["invalid measurement"] = str(line_num + 1)


        if name in clean_ingredients:
            validation_error = True
            if "duplicated ingredients" in errors:
                errors["duplicated ingredients"] += ', ' + str(line_num + 1)
            else:
                errors["duplicated ingredients"] = str(line_num + 1)
            
        if validation_error:
            continue
        
        clean_ingredients[name] = (quantity_float, measure)


    if errors:
        raise ValidationError(errors=errors)

    return clean_ingredients