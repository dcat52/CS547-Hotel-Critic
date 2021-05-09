from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import TextField, ValidationError, SubmitField, FormField, validators
from wtforms.validators import Required

class SearchForm(FlaskForm):
    qfield = TextField('Search Query')
    lfield = TextField('Location Filter')

    submit_button = SubmitField('Search')
