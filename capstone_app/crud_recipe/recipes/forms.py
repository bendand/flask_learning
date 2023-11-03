from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import ValidationError
## user based imports 



class RecipeForm(FlaskForm):

    # measurement_choices = ['cup', 'teaspoon', 'tablespoon', 'count', 'pint']

    recipe_name = StringField('Recipe Name', validators=[DataRequired()])
    enter_ingredients = TextAreaField('Enter the ingredient, the quantity, and the measurement, with each value separated by a comma. Ex: "rice, 1, cup"', validators=[DataRequired()])

    # quantity = IntegerField('Insert a numeric quantity', validators=[DataRequired()])
    # measurement = SelectField('Unit of Measurement', choices=measurement_choices, validators=[DataRequired()])
    # enter_ingredient = SubmitField('Enter Ingredient')
    enter_recipe = SubmitField('Submit All Ingredients')