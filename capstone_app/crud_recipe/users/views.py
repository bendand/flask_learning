from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from crud_recipe import db
from crud_recipe.mockup_function import recipe_processor
from werkzeug.security import generate_password_hash,check_password_hash
from crud_recipe.models import User, Ingredient, Recipe, RecipeToIngredient
from crud_recipe.users.forms import RegistrationForm, LoginForm, UpdateUserForm, AddIngredientsForm
from flask.json import jsonify

import pint
from simple_test import test
from pint import UnitRegistry
from pint.errors import UndefinedUnitError

## to discuss

# import requests

# r = requests.get("http://google.com")       
# print(r.status_code)



users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
    return render_template('login.html', form=form)




@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

        return render_template('account.html', form=form)


@users.route("/generatelist", methods=['GET', 'POST'])
def create_list():

    recipe_form = AddIngredientsForm()

    if recipe_form.validate_on_submit():

        recipe_name = recipe_form.recipe_name

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

                # then save the ingredient as a record in the recipe to ingredient table
                recipe_to_ingredient = RecipeToIngredient(ingredient_quantity=int(item[1]), ingredient_measurement=item[2])

                # commit both
                # db.session.add(ingredient, recipe_to_ingredient)
                # db.session.commit()

            # if the ingredient name is already in the ingredient table...
            else:

                # just save the ingredient as a record in the recipe to ingredient table
                recipe_to_ingredient = RecipeToIngredient(ingredient_quantity=int(item[1]), ingredient_measurement=item[2])

                # then commit both
                # db.session.add(recipe_to_ingredient)
                # db.session.commit()


            # should i flash a two-button form that asks the user if they want to either enter 
            return redirect(url_for('users.view_users_recipes', username=current_user.username))


    return render_template('create_shopping_list.html', form=recipe_form)




    
# @users.route("/viewlist", methods=['GET'])
# def view_list():

#     query = db.session.query(Ingredient).all()
    
#     presentable = [ingredient.to_dict() for ingredient in query]

#     jsonified = jsonify(presentable)

#     return jsonified

'''is a view shopping lists view necessary? whats this supposed to look like? 
should a person be able to make multiple lists and view them from the view_shopping_lists view?  '''


@users.route("/<username>")
def view_users_recipes(username):
    ## this should list each post with a date and a recipe title and show a date timestamp ##
    user = User.query.filter_by(username=username).first_or_404()
    recipes = Recipe.query.filter_by(creator=user).order_by(Recipe.date.desc())

    return render_template('users_recipes.html', recipes=recipes,  user=user)





# query = db.session.query(Ingredient).all()
    
#     presentable = [ingredient.to_dict() for ingredient in query]

#     jsonified = jsonify(presentable)

#     return jsonified



