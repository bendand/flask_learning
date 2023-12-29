from flask import render_template,url_for,flash,redirect,request,Blueprint,abort
from flask_login import current_user,login_required
from crud_recipe import db
from crud_recipe.models import Ingredient,Recipe,RecipeToIngredient,User
from crud_recipe.recipes.forms import RecipeForm
import datetime
from sqlalchemy import select,delete
from pint import UnitRegistry, DimensionalityError

recipe_views = Blueprint('recipes',__name__, url_prefix='/recipes')


@recipe_views.route("/add", methods=['GET', 'POST'])
@login_required
def add_recipe():

    recipe_form = RecipeForm()
    title = 'Adding a Recipe'

    if not recipe_form.validate_on_submit():

        return render_template('enter_recipe.html', form=recipe_form, title=title)


    recipe_name = recipe_form.recipe_name.data

    new_recipe = Recipe(name=recipe_name, user_id=current_user.id)

    # grabs the data from the enter ingredients field, splits it into lines, and makes it moldable
    recipe_data = recipe_form.enter_ingredients.data.splitlines()

    # initialize our validation error message dictionary
    errors = {}
    # repository for clean ingredients
    clean_ingredients = {}

    for line_num, line in enumerate(recipe_data):
        
        raw_ingredient = line.split(', ')
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

    print(clean_ingredients)

    if errors:
        return render_template('enter_recipe.html', form=recipe_form, errors=errors.items())

    

    # we add and commit our recipe knowing now that our points of validation check out
    db.session.add(new_recipe)
    db.session.commit()


    for ingredient_name, quantity_measurement in clean_ingredients.items():
        
        ingredient_quantity = quantity_measurement[0]
        ingredient_measurement = quantity_measurement[1]
    
        # produces a name or a none value in this variable
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()

        # if the ingredient is not in the ingredient table...
        if not ingredient:

            # create an instance of ingredient and commit 
            ingredient = Ingredient(name=ingredient_name)

            db.session.add(ingredient)
            db.session.commit()

        # this then needs to be done regardless of whether or not the ingredient has been added to our database before
        recipe_to_ingredient = RecipeToIngredient(recipe_id=new_recipe.id,
                                                ingredient_id=ingredient.id, 
                                                ingredient_quantity=ingredient_quantity, 
                                                ingredient_measurement=ingredient_measurement)

        db.session.add(recipe_to_ingredient)
        db.session.commit()
        

    success_message = 'your recipe, ' + recipe_name + ', was added!'
    return render_template('enter_recipe.html', form=recipe_form, success_message=success_message)


@recipe_views.route("/generatelist/<username>")
def generate_shopping_list(username):
    
    user = User.query.filter_by(username=username).first_or_404()
    recipes = Recipe.query.filter_by(user_id=user.id).all()

    return render_template('generate_shopping_list.html', recipes=recipes)



# int: makes sure that the recipe_id gets passed as in integer
# instead of a string so we can look it up later.
@recipe_views.route('/<int:recipe_id>')
def recipe_view(recipe_id):
    # grab the requested recipe by id number or return 404
    recipe = Recipe.query.get_or_404(recipe_id)
    # need some way below here to make all the ingredients in the recipe given above available for enumeration in html
    recipe_ingredients_query = (
                        db.session.query(Ingredient.name, RecipeToIngredient.ingredient_quantity, RecipeToIngredient.ingredient_measurement)
                        .join(Ingredient, RecipeToIngredient.ingredient_id == Ingredient.id)
                        .where(RecipeToIngredient.recipe_id == recipe.id)
                        )
    # print(recipe_ingredients_query)
    recipe_ingredients = recipe_ingredients_query.all()
    return render_template('recipe.html', recipe_name=recipe.name,
                            submit_date=recipe.date, recipe=recipe, recipe_ingredients=recipe_ingredients)

@recipe_views.route("/<int:recipe_id>/update", methods=['GET', 'POST'])
@login_required
def update(recipe_id):

    old_recipe = Recipe.query.get_or_404(recipe_id)
    update_recipe_form = RecipeForm()
    title = 'Update Recipe'

    if not update_recipe_form.validate_on_submit():
        
        update_recipe_form.recipe_name.data = old_recipe.name

        return render_template('enter_recipe.html', form=update_recipe_form, title=title, recipe_name=update_recipe_form.recipe_name.data)

    # initialize our validation error message dictionary with none values
    error_dict = {"tuple_length_error_message": None, "quantity_type_error_message": None, 
                  "measurement_error_message": None, "duplicated_items_error_message": None}

    recipe_name = update_recipe_form.recipe_name.data

    updated_recipe = Recipe(name=recipe_name, user_id=current_user.id)

    # grabs the data from the enter ingredients field, splits it into lines, and makes it moldable
    recipe_data = update_recipe_form.enter_ingredients.data.splitlines()

    # initialize our validation error message dictionary
    errors = {}
    # repository for clean ingredients
    clean_ingredients = {}
    
    for line_num, line in enumerate(recipe_data):
        
        raw_ingredient = line.split(', ')
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
            return render_template('enter_recipe.html', form=update_recipe_form, errors=errors.items())
            
    # deletes our old recipe and all of our ingredients that are linked to the old recipe
    db.session.delete(old_recipe)
    delete_old_ingredients_stmt = delete(RecipeToIngredient).where(RecipeToIngredient.recipe_id==old_recipe.id)
    db.session.execute(delete_old_ingredients_stmt)

    # now we add and commit the new one
    db.session.add(updated_recipe)
    db.session.commit()

    for ingredient_name, quantity_measurement in clean_ingredients.items():
        
        ingredient_quantity = quantity_measurement[0]
        ingredient_measurement = quantity_measurement[1]
    
        # produces a name or a none value in this variable
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()

        # if the ingredient is not in the ingredient table...
        if not ingredient:

            # create an instance of ingredient and commit 
            ingredient = Ingredient(name=ingredient_name)

            db.session.add(ingredient)
            db.session.commit()

        # this then needs to be done regardless of whether or not the ingredient has been added to our database before
        recipe_to_ingredient = RecipeToIngredient(recipe_id=updated_recipe.id,
                                                ingredient_id=ingredient.id, 
                                                ingredient_quantity=ingredient_quantity, 
                                                ingredient_measurement=ingredient_measurement)

        db.session.add(recipe_to_ingredient)
        db.session.commit()

    success_message = 'your recipe, ' + recipe_name + ', was updated!'
    return render_template('enter_recipe.html', form=update_recipe_form, success_message=success_message)
    


@recipe_views.route("/<int:recipe_id>/delete", methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    delete_recipe_stmt = delete(Recipe).where(Recipe.id == recipe.id)
    delete_recipe_ingredients_stmt = delete(RecipeToIngredient).where(RecipeToIngredient.recipe_id == recipe.id)
    
    db.session.execute(delete_recipe_stmt)
    db.session.execute(delete_recipe_ingredients_stmt)
    db.session.commit()

    updated_user_recipes = Recipe.query.filter_by(user_id=current_user.id).all()

    message = 'Recipe deleted'

    return render_template('user_recipes.html', message=message, user=current_user, recipes=updated_user_recipes)