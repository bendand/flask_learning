import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

## imports for add_ingredients

import pint
from simple_test import test
from pint import UnitRegistry
from pint.errors import UndefinedUnitError


app = Flask(__name__)


app.config['SECRET_KEY'] = 'mysecret'

#################################
### DATABASE SETUPS ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app,db)

###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = 'users.login'



from crud_recipe.core.views import core
from crud_recipe.users.views import users
from crud_recipe.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)


ureg = UnitRegistry()

def add_ingredients(recipe):
    ureg = UnitRegistry()
    ingr_dict = {}
    for ingredient in recipe:
        item = ingredient[0]
        quantity = ingredient[1]
        msmt = ingredient[2]
        try:
            quantity_msmt = quantity * ureg(msmt)
            if item in ingr_dict:
                ingr_dict[item] += quantity_msmt
            else:
                ingr_dict[item] = quantity_msmt
        except UndefinedUnitError:
            quantity_msmt2 = quantity, msmt
            if item in ingr_dict:
                ingr_dict[item] += quantity_msmt2
            else:
                ingr_dict[item] = quantity_msmt2

    return ingr_dict


# some_recipe = [("rice", 1, "cup"), ("salt", 1, "tsp"),
#                ("rice", 1/4, "cup"), ("garlic cloves", 2, "count"), ("salt", 5, "tbsp"), ("garlic cloves", 2, "count")]

# test(add_ingredients(
#     [("rice", 1, "cup"),
#      ("salt", 1, "tsp"),
#      ("rice", 1/4, "cup"), ("garlic cloves", 2, "count"), ("salt", 5, "tbsp"), ("garlic cloves", 2, "count")]) == {'rice': 1.25 * ureg('cup'), 'salt': 16.0 * ureg('teaspoon'), 'garlic cloves': 4 * ureg('count')})


