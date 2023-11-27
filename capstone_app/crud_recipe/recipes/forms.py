from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import ValidationError
## user based imports 



class RecipeForm(FlaskForm):

    recipe_name = StringField('Recipe Name', validators=[DataRequired()])
    enter_ingredients = TextAreaField('Enter the ingredient, the quantity, and the measurement, with each value separated by a comma. Ex: "rice, 1, cup"', validators=[DataRequired()])

    enter_recipe = SubmitField('Submit All Ingredients')