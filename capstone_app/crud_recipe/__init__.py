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
from crud_recipe.users.views import user_views
from crud_recipe.error_pages.handlers import error_pages
from crud_recipe.recipes.views import recipe_views


app.register_blueprint(core)
app.register_blueprint(user_views)
app.register_blueprint(error_pages)
app.register_blueprint(recipe_views)


