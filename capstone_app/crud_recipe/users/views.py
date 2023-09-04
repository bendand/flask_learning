from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from crud_recipe import db
from werkzeug.security import generate_password_hash,check_password_hash
from crud_recipe.models import User, Ingredient, Recipe
from crud_recipe.users.forms import RegistrationForm, LoginForm, UpdateUserForm, CreateShoppingListForm, AddIngredientForm


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
        if form.picture.data:
            username = current_user.username

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template(url_for('account.html', form=form))


@users.route("/generatelist", methods=['GET', 'POST'])
def create_list():

    ingredient_1 = Ingredient(1, 'garlic clove')
    db.session.add(ingredient_1)

    ingredient_2 = Ingredient(2, 'sugar')
    db.session.add(ingredient_2)

    ingredient_3 = Ingredient(3, 'salt')
    db.session.add(ingredient_3)

    ingredient_4 = Ingredient(4, 'beans')
    db.session.add(ingredient_4)

    db.session.commit()

    query = db.session.query(Ingredient).all()

    print(query)
    return query

    

    # db.session.commit()

    # the_query = db.session.query(Ingredient).all()

    # return the_query
    

    # ingredient_list = []

    # form = CreateShoppingListForm()

    # if form.validate_on_submit():
    #     recipe = Recipe(name=form.name.data)
    #     return redirect(url_for('users.add_ingredients'))

    # return render_template('generate_list.html')

'''is a view shopping lists view necessary? whats this supposed to look like? 
should a person be able to make multiple lists and view them from the view_shopping_lists view?  '''

@users.route("/addingredients", methods=['GET,' 'POST'])
def add_ingredients():
    pass

    # form = AddIngredientForm

    # if form.validate_on_submit():
    #     ingredient = Ingredient(name=form.name.data)

    #     db.session.add(ingredient)
    #     db.session.commit()
    #     flash('Ingredient Added')
    #     return redirect(url_for('users.account'))




@users.route("/shoppinglists", methods=['GET'])
def view_shopping_lists():
    ## this should list each post with a date and a recipe title and show a date timestamp ## 
    pass








