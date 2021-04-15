"""
    Example Controllers
"""

from flask import render_template, redirect, url_for
from flask_wtf import FlaskForm

from project import app
from project.models.Hotel import Hotel
from project.models.SearchForm import SearchForm


#route index
@app.route('/submit', methods=['POST'])
def search(submit=False):
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

    return render_template('index.html.j2', data=data, form=form, hotels=hotels)
