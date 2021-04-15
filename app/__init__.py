from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required


class ExampleForm(FlaskForm):
    field1 = TextField('Search Query')

    submit_button = SubmitField('Search')

class Person:
    def __init__(self, rank, rating, name, location):
        self.rank = rank
        self.rating = rating
        self.name = name
        self.location = location

def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    @app.route('/', methods=('GET', 'POST'))
    def index():
        form = ExampleForm()
        form.validate_on_submit()
        people = []
        p1 = Person(1, 4.8, "Higgins", "WPI")
        p2 = Person(2, 4.5, "Salisbury", "WPI")
        p3 = Person(3, 1.2, "Sketchy", "Nowhere")
        p4 = Person(4, 1.1, "Super Sketchy", "Nowhere")
        people = [p1, p2, p3, p4]
        return render_template('index.html', form=form, people=people)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
