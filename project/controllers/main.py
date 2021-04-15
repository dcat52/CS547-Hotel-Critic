"""
    Example Controllers
"""

from flask import render_template, redirect, url_for
from flask_wtf import FlaskForm

from project import app
from project.models.Hotel import Hotel
from project.models.SearchForm import SearchForm

def get_version_string():
    version_str = "Vers. {}".format(app.__version__)
    return version_str

@app.route('/about', methods=['GET'])
def about():
    text = "It is an app.<br>Developed by student.<br>While at Worcester Polytechnic Institute.<br><a href='https://github.com/dcat52/CS547_Hotel_Critic'>See it on Github</a>"
    version_str = get_version_string()
    return render_template('about.html.j2', vers=version_str, text=text)


@app.route('/submit', methods=['POST'])
def search():
    return index(submit=True)

#route index
@app.route('/', methods=['GET'])
def index(submit=False):
    data = {
        "title": "Hello World",
        "body": "Flask simple MVC"
    }
    form = SearchForm()
    form.validate_on_submit()

    p1 = Hotel(1, 4.8, "Higgins", "WPI")
    p2 = Hotel(2, 4.5, "Salisbury", "WPI")
    p3 = Hotel(3, 1.2, "Sketchy", "Nowhere")
    p4 = Hotel(4, 1.1, "Super Sketchy", "Nowhere")
    hotels = [p1, p2, p3, p4]

    if submit:
        i = 0
        while i < len(hotels):
            if form.qfield.data not in hotels[i].name:
                hotels.pop(i)
            else:
                i += 1

    version_str = get_version_string()

    return render_template('index.html.j2', vers=version_str, form=form, hotels=hotels)
