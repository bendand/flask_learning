from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from crud_recipe import db
from werkzeug.security import generate_password_hash,check_password_hash
from crud_recipe.models import User, Ingredient, Recipe
from crud_recipe.users.forms import RegistrationForm, LoginForm, UpdateUserForm, CreateShoppingListForm, AddIngredientForm
from flask.json import jsonify



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

    ## here im trying to ask for a recipe name to store all the ingredients and their measurements/quantities under
    ## then i want to redirect to a different form to ask prompt the user to input the ingredients and their msmts
    ## im going to have to work out how to add this recipe in its correct form to my database and have all my 
    ## dependencies and backreferences line up 

    ## how to prevent circular redirection errors? 

    create_form = CreateShoppingListForm()

    ## how do i feature id as being part of this recipe? how to include attributes that are already auto_incremented is tricky

    if create_form.validate_on_submit():
        shopping_list = Recipe(name=create_form.name.data,
                               user_id=current_user.id)

    #     ## ^ is this the right syntax? since recipes.id is auto-incremented it doesn't need to be declared right?

        db.session.add(shopping_list)
        db.session.commit()
        flash('Recipe Added!')

        ## where do i go from here? Just go straight to the next form? 

        ## where is the other info like quantity and measurement stored in the data tables? Should they just be featured 
        ## in my recipes table that lists ingredients in the tables?

        ingredient_form = AddIngredientForm()

        if ingredient_form.validate_on_submit:
            ingredient = Ingredient()

        # form = AddIngredientForm()

        # if form.validate_on_submit():
        #     ingredient = Ingredient(id=form.id.data, 
        #                             name=form.name.data)

        #     db.session.add(ingredient)
        #     db.session.commit()
        #     flash('Ingredient Added')
        #     return redirect(url_for('users.create_list'))

    return render_template('create_shopping_list.html', form=create_form)


    # query = db.session.query(Ingredient).all()
    
    # presentable = [ingredient.to_dict() for ingredient in query]

    # jsonified = jsonify(presentable)

    # return jsonified

    
@users.route("/viewlist", methods=['GET'])
def view_list():

    query = db.session.query(Ingredient).all()
    
    presentable = [ingredient.to_dict() for ingredient in query]

    jsonified = jsonify(presentable)

    return jsonified



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








