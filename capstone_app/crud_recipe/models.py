from crud_recipe import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))


    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"



class Ingredient(db.Model):

    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)     ## are any validators/conditionals required here or are none needed?

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):    ## is the __repr__ function used for getting the data in the right form to be passed through functions?
        return f"id: {self.id} --- name: {self.name}"


class Recipe(db.Model):

    __tablename__ = 'recipes'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, id, name, user_id):
        self.id = id
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f"id: {self.id} --- name: {self.name} --- user id: {self.user_id}"


class RecipeToIngredient(db.Model):      

    __tablename__ = 'recipe_to_ingredient'


    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    ingredient_quantity = db.Column(db.Integer)
    ingredient_measurement = db.Column(db.String(50))



# class RecipeToRecipe(db.Model):

#     __tablename__ = 'recipe_to_recipe'

#     id = db.Column(db.ForeignKey('recipes.id', 'recipes.id'), primary_key=True)
#     recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
#     recipe_name = db.Column(db.String(100), db.ForeignKey('recipes.name'))
#     recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
#     recipe_name = db.Column(db.String(100), db.ForeignKey('recipes.name'))



# users = db.Table(
#     "users",
#     db.Column("id", db.ForeignKey('users.id')),
#     db.Column("email", db.ForeignKey('users.email')),
#     db.Column("username", db.ForeignKey('users.username')),
# )


# ingredients = db.Table(
#     "ingredients",
#     db.Column("id", db.ForeignKey('ingredients.id')),
#     db.Column("name", db.ForeignKey('ingredients.name')),
# )



# recipes = db.Table(
#     "recipes",
#     db.Column("id", db.ForeignKey('recipes.id')),
#     db.Column("name", db.ForeignKey('recipes.name')),
#     db.Column("user_id", db.ForeignKey('recipes.user_id')),
# )