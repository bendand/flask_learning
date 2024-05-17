from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):
    ingredient = StringField('Ingredient', DataRequired())
    submit = SubmitField('Add Ingredient')