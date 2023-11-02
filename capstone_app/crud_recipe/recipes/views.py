from flask import render_template,url_for,flash,redirect,request,Blueprint,abort
from flask_login import current_user,login_required
from crud_recipe import db
from crud_recipe.models import Ingredient,Recipe,RecipeToIngredient
from crud_recipe.recipes.forms import RecipeForm
import datetime

recipes = Blueprint('recipes',__name__)


@recipes.route("/addrecipe", methods=['GET', 'POST'])
@login_required
def add_recipe():

    recipe_form = RecipeForm()

    if recipe_form.validate_on_submit():

        recipe_name = recipe_form.recipe_name.data

        new_recipe = Recipe(name=recipe_name, user_id=current_user.username)

        db.session.add(new_recipe)
        db.session.commit()

        # grabs the data from the enter ingredients field, splits it into lines, and makes it moldable
        recipe_data = recipe_form.enter_ingredients.data.splitlines()

        # splits into 3 items per line, no whitespace, with a comma separating each value
        recipe_items = [item.split(', ') for item in recipe_data]

        # converts each item in the list into a tuple
        new_recipe_items = [tuple(item) for item in recipe_items]

        for item in new_recipe_items:

            # creates an in_database variable with a name or a 'None' value
            in_database = Ingredient.query.filter_by(name=item[0]).first()

            # if the ingredient name is not in the ingredient table...
            if in_database == None:

                # save the ingredient to the ingredient table
                ingredient = Ingredient(name=item[0])

                db.session.add(ingredient)
                db.session.commit()

                # then save the ingredient as a record in the recipe to ingredient table
                recipe_to_ingredient = RecipeToIngredient(recipe_id=new_recipe.id,
                                                          ingredient_id=ingredient.id, 
                                                          ingredient_quantity=int(item[1]), 
                                                          ingredient_measurement=item[2])

                db.session.add(recipe_to_ingredient)
                db.session.commit()

            # if the ingredient name is already in the ingredient table...
            else:

                ingredient = Ingredient.query.filter_by(name=item[0]).first()


                recipe_to_ingredient = RecipeToIngredient(recipe_id=new_recipe.id, 
                                                          ingredient_id=ingredient.id,
                                                          ingredient_quantity=int(item[1]),
                                                          ingredient_measurement=item[2])

                db.session.add(recipe_to_ingredient)
                db.session.commit()


            # should i flash a two-button form that asks the user if they want to either enter another recipe or 'go to my recipes'?
            flash('Recipe added to My Recipes')
            return redirect(url_for('recipes.add_recipe'))


    return render_template('enter_recipe.html', form=recipe_form)



# int: makes sure that the blog_post_id gets passed as in integer
# instead of a string so we can look it up later.
@recipes.route('/<int:recipe_id>')
def recipe(recipe_id):
    # grab the requested recipe by id number or return 404
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', recipe_name=recipe.name,
                            submit_date=recipe.date, recipe_id=recipe_id)

@recipes.route("/<int:recipe_id>/update", methods=['GET', 'POST'])
@login_required
def update(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        # Forbidden, No Access
        abort(403)

    form = RecipeForm()
    if form.validate_on_submit():
        recipe.name = form.recipe_name.data
        recipe.ingredients = form.enter_ingredients.data
        db.session.commit()
        flash('Recipe Updated')
        return redirect(url_for('recipe.recipe', recipe_id=recipe.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.recipe_name.data = recipe.name
        form.enter_ingredients.data = recipe.ingredients
    return render_template('create_post.html', title='Update',
                           form=form)


@recipes.route("/<int:recipe_id>/delete", methods=['POST'])
@login_required
def delete_post(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe has been deleted')
    return redirect(url_for('core.index'))