from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from crud_recipe import db
from crud_recipe.reducer_function import recipe_reducer
from werkzeug.security import generate_password_hash,check_password_hash
from crud_recipe.models import User, Ingredient, Recipe, RecipeToIngredient
from crud_recipe.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from flask.json import jsonify
from crud_recipe.users.forms import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo



import pint
from simple_test import test
from pint import UnitRegistry
from pint.errors import UndefinedUnitError

## to discuss

# import requests

# r = requests.get("http://google.com")       
# print(r.status_code)



user_views = Blueprint('users', __name__, url_prefix='/users')

@user_views.route('/register', methods=['GET', 'POST'])
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

@user_views.route('/login', methods=['GET', 'POST'])
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




@user_views.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@user_views.route("/account", methods=['GET', 'POST'])
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


# @users.route("/viewlist", methods=['GET'])
# def view_list():

#     query = db.session.query(Ingredient).all()
    
#     presentable = [ingredient.to_dict() for ingredient in query]

#     jsonified = jsonify(presentable)

#     return jsonified

'''is a view shopping lists view necessary? whats this supposed to look like? 
should a person be able to make multiple lists and view them from the view_shopping_lists view?  '''


@user_views.route("/<username>")
def view_users_recipes(username):
    
    user = User.query.filter_by(username=username).first_or_404()
    recipes = Recipe.query.filter_by(user_id=user.id).order_by(Recipe.date.desc()).all()

    return render_template('user_recipes.html', recipes=recipes,  user=user)


@user_views.route("/<username>/generatelist", methods=['GET', 'POST'])
def generate_shopping_list(username):

    if request.method == 'GET': 
   
        user = User.query.filter_by(username=username).first_or_404()
        recipes = Recipe.query.filter_by(user_id=user.id).order_by(Recipe.date.desc()).all()

        return render_template('generate_shopping_list.html', recipes=recipes, current_user=user)

    if request.method == 'POST':

        form_items = request.form.items()

        recipe_id_list = []

        for k, v in form_items:
            recipe_id = int(k)
            recipe_id_list.append(recipe_id)

        # finds all ingredients from a list of recipe ids
        recipe_ingredients_result = (
                    db.session.query(Ingredient.name, RecipeToIngredient.ingredient_quantity, RecipeToIngredient.ingredient_measurement)
                    .join(Ingredient, RecipeToIngredient.ingredient_id == Ingredient.id)
                    .where(RecipeToIngredient.recipe_id.in_(recipe_id_list))
                    ).all()
        

        # variable holds the returned result of our reducer function 
        shopping_list_ingredients = recipe_reducer(recipe_ingredients_result)

        # sorting our items alphabetically
        sorted_ingredients = sorted(shopping_list_ingredients)
 
        return render_template('new_shopping_list.html', shopping_list_ingredients=sorted_ingredients)





# query = db.session.query(Ingredient).all()
    
#     presentable = [ingredient.to_dict() for ingredient in query]

#     jsonified = jsonify(presentable)

#     return jsonified



