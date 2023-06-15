# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AddForm(FlaskForm):

    name = StringField('name of puppy')
    submit = SubmitField('add puppy')


class AddOwnerForm(FlaskForm):

    name = StringField('Name of Owner:')
    pup_id = IntegerField("Id of Puppy: ")
    submit = SubmitField('Add Owner')


class DelForm(FlaskForm):

    id = IntegerField("Id number of puppy to remove: ")
    submit = SubmitField("remove puppy")
