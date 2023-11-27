from flask import render_template,url_for,flash,redirect,request,Blueprint,abort
from flask_login import current_user,login_required
from crud_recipe import db
from crud_recipe.models import Ingredient,Recipe,RecipeToIngredient,User
from crud_recipe.recipes.forms import RecipeForm
import datetime
from sqlalchemy import select,delete
from pint import UnitRegistry

recipe_views = Blueprint('recipes',__name__, url_prefix='/recipes')


@recipe_views.route("/add", methods=['GET', 'POST'])
@login_required
def add_recipe():

    recipe_form = RecipeForm()
    title = 'Adding a Recipe'

    if recipe_form.validate_on_submit():

        recipe_name = recipe_form.recipe_name.data

        new_recipe = Recipe(name=recipe_name, user_id=current_user.id)

        # grabs the data from the enter ingredients field, splits it into lines, and makes it moldable
        recipe_data = recipe_form.enter_ingredients.data.splitlines()

        # splits into 3 items per line, no whitespace, with a comma separating each value
        recipe_items = [item.split(', ') for item in recipe_data]

        # converts each item in the list into a tuple
        new_recipe_items = [tuple(item) for item in recipe_items]

        #establishes some instances/variables so we can check to see if the user is inputting valid measurements
        ureg = UnitRegistry()
        ureg_offenders = []
        not_in_registry = 0

        # checks for belonging in our registry
        for item in new_recipe_items:

            measurement = item[2]

            if measurement not in ureg:

                ureg_offenders.append(measurement)
                not_in_registry += 1

        # if we have one instance of unbelonging we redirect the user to a blank form with an error message
        if not_in_registry > 0:

            message = 'your units of measure: ' + str(ureg_offenders) + ' are invalid'
            return(render_template('enter_recipe.html', form=recipe_form, message=message))

        else:

            # we add and commit our recipe knowing now that our units of measurent work
            db.session.add(new_recipe)
            db.session.commit()

            for item in new_recipe_items:

                # establishes convenient names for our indexed values
                item_name = item[0]
                item_quantity = float(item[1])
                item_measurement = item[2]

                # produces a name or a none value in this variable
                in_database = Ingredient.query.filter_by(name=item_name).first()

                # if the ingredient is not in the ingredient table...
                if in_database == None:

                    # create an instance of ingredient and commit 
                    new_ingredient = Ingredient(name=item_name)

                    db.session.add(new_ingredient)
                    db.session.commit()

                    # then save the ingredient as a record in the recipe to ingredient table
                    recipe_to_ingredient = RecipeToIngredient(recipe_id=new_recipe.id,
                                                            ingredient_id=new_ingredient.id, 
                                                            ingredient_quantity=item_quantity, 
                                                            ingredient_measurement=item_measurement)

                    db.session.add(recipe_to_ingredient)
                    db.session.commit()

                # if the ingredient name is already in the ingredient table...
                else:

                    ingredient_in_database = Ingredient.query.filter_by(name=item_name).first()

                    recipe_to_ingredient = RecipeToIngredient(recipe_id=new_recipe.id, 
                                                            ingredient_id=ingredient_in_database.id,
                                                            ingredient_quantity=item_quantity,
                                                            ingredient_measurement=item_measurement)

                    db.session.add(recipe_to_ingredient)
                    db.session.commit()

            message = 'your recipe, ' + recipe_name + ', was added!'
            return render_template('enter_recipe.html', form=recipe_form, message=message)
                # should i flash a two-button form that asks the user if they want to either enter another recipe or 'go to my recipes'?
                # return redirect(url_for('recipes.add_recipe')

    return render_template('enter_recipe.html', form=recipe_form, title=title)

@recipe_views.route("/generatelist/<username>")
def generate_shopping_list(username):
    
    user = User.query.filter_by(username=username).first_or_404()
    recipes = Recipe.query.filter_by(user_id=user.id).all()

    # print(recipes)

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

    if update_recipe_form.validate_on_submit():

        recipe_name = update_recipe_form.recipe_name.data

        updated_recipe = Recipe(name=recipe_name, user_id=current_user.id)

        # grabs the data from the enter ingredients field, splits it into lines, and makes it moldable
        recipe_data = update_recipe_form.enter_ingredients.data.splitlines()

        # splits into 3 items per line, no whitespace, with a comma separating each value
        recipe_items = [item.split(', ') for item in recipe_data]

        # converts each item in the list into a tuple
        new_recipe_items = [tuple(item) for item in recipe_items]

        #establishes some instances/variables so we can check to see if the user is inputting valid measurements
        ureg = UnitRegistry()
        ureg_offenders = []
        not_in_registry = 0

        # checks for belonging in our registry
        for item in new_recipe_items:

            measurement = item[2]

            if measurement not in ureg:

                ureg_offenders.append(measurement)
                not_in_registry += 1

        # if we have one instance of unbelonging we redirect the user to a blank form with an error message
        if not_in_registry > 0:

            message = 'your units of measure: ' + str(ureg_offenders) + ' are invalid'
            return(render_template('enter_recipe.html', form=update_recipe_form, message=message))

        else:

            # we add and commit our recipe knowing now that our units of measurent work
            # should we delete the old recipe like written below?
            db.session.delete(old_recipe)
            db.session.add(updated_recipe)

            db.session.commit()

            for item in new_recipe_items:

                # establishes convenient names for our indexed values
                item_name = item[0]
                item_quantity = float(item[1])
                item_measurement = item[2]

                # produces a name or a none value in this variable
                in_database = Ingredient.query.filter_by(name=item_name).first()

                # if the ingredient is not in the ingredient table...
                if in_database == None:

                    # create an instance of ingredient and commit 
                    new_ingredient = Ingredient(name=item_name)

                    db.session.add(new_ingredient)
                    db.session.commit()

                    # then save the ingredient as a record in the recipe to ingredient table
                    recipe_to_ingredient = RecipeToIngredient(recipe_id=updated_recipe.id,
                                                            ingredient_id=new_ingredient.id, 
                                                            ingredient_quantity=item_quantity, 
                                                            ingredient_measurement=item_measurement)

                    db.session.add(recipe_to_ingredient)
                    db.session.commit()

                # if the ingredient name is already in the ingredient table...
                else:

                    ingredient_in_database = Ingredient.query.filter_by(name=item_name).first()

                    recipe_to_ingredient = RecipeToIngredient(recipe_id=updated_recipe.id, 
                                                            ingredient_id=ingredient_in_database.id,
                                                            ingredient_quantity=item_quantity,
                                                            ingredient_measurement=item_measurement)

                    db.session.add(recipe_to_ingredient)
                    db.session.commit()

            message = 'your recipe, ' + recipe_name + ', was updated!'

        db.session.commit()
        flash('Recipe Updated')
        return redirect(url_for('recipe_views.recipe_view', recipe_id=updated_recipe.id))
    # Pass back the old recipe information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        update_recipe_form.recipe_name.data = old_recipe.name
    return render_template('enter_recipe.html', title=title,
                           form=update_recipe_form)


@recipe_views.route("/<int:recipe_id>/delete", methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    #needs here to also delete ingredients linked to the recipe id 
    delete_recipe_stmt = delete(Recipe).where(Recipe.id == recipe.id)
    delete_recipe_ingredients_stmt = delete(RecipeToIngredient).where(RecipeToIngredient.recipe_id == recipe.id)
    
    db.session.execute(delete_recipe_stmt)
    db.session.execute(delete_recipe_ingredients_stmt)
    db.session.commit()

    updated_user_recipes = Recipe.query.filter_by(user_id=current_user.id).all()

    message = 'Recipe deleted'
    # need to figure out how to pass in this message
    return render_template('user_recipes.html', message=message, user=current_user, recipes=updated_user_recipes)