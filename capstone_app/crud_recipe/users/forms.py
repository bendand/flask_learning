from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
## user based imports 
from flask_login import current_user
from crud_recipe.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has been registered already!')


class UpdateUserForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Update')

    def check_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user != current_user:
            raise ValidationError('A user with that email already exists.')

    def check_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and user != current_user:
            raise ValidationError('This username is taken')


class ShoppingListForm(FlaskForm):

    ingredient = StringField('Ingredient', validators=[DataRequired()])
    quantity = IntegerField('Insert a numeric quantity', validators=[DataRequired()])
    measurement = StringField('Unit of Measurement', validators=[DataRequired()])
    enter_ingredient = SubmitField('Enter Ingredient')
    submit = SubmitField('Generate my Shopping List')