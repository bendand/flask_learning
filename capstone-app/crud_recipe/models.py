from crud_recipe import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from flask_login import UserMixin
from datetime import datetime
from dataclasses import dataclass
from flask.json import jsonify

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@dataclass
class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
        return f"ID: {self.id} -- Email: {self.email} Userame: {self.username}"


@dataclass
class Ingredient(db.Model):

    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)     ## are any validators/conditionals required here or are none needed?

    def __init__(self, name):
        self.name = name

    def __repr__(self):  
        return f"id: {self.id} --- name: {self.name}"

    
    def to_dict(self):
        return {"id": self.id,
                "name": self.name}


@dataclass
class Recipe(db.Model):

    __tablename__ = 'recipes'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f"id: {self.id} --- name: {self.name} --- date: {self.date}"

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "user id": self.date,
                "date": self.date}


#does my recipetoingredient model need this dataclass tag?
@dataclass
class RecipeToIngredient(db.Model):      

    __tablename__ = 'recipe_to_ingredient'


    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    ingredient_quantity = db.Column(db.Integer)
    ingredient_measurement = db.Column(db.String(50))


    def __init__(self, recipe_id, ingredient_id, ingredient_quantity, ingredient_measurement):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.ingredient_quantity = ingredient_quantity
        self.ingredient_measurement = ingredient_measurement


    def __repr__(self):
        return f"recipe id: {self.recipe_id} --- ingredient id: {self.ingredient_id} --- ingredient quantity: {self.ingredient_quantity} --- ingredient measurement: {self.ingredient_measurement}"


    def to_dict(self):
        return {"recipe id": self.recipe_id,
                "ingredient id": self.ingredient_id,
                "ingredient quantity": self.ingredient_quantity,
                "ingredient measurement": self.ingredient_measurement}




