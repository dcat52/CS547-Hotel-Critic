"""
    Example Controllers
"""

from flask import render_template, redirect, url_for
from flask_wtf import FlaskForm

from project import app
from project.models.Hotel import Hotel
from project.models.SearchForm import SearchForm
# from project.controllers.DataPreprocess import *
from project.controllers.QueryProcess import parse_location, cal_final_score

def get_version_string():
    version_str = "Vers. {}".format(app.__version__)
    return version_str

@app.route('/about', methods=['GET'])
def about():
    text = "It is an app.<br>Developed by students.<br>While at Worcester Polytechnic Institute.<br><a href='https://github.com/dcat52/CS547_Hotel_Critic'>See it on Github</a>"
    version_str = get_version_string()
    return render_template('about.html.j2', vers=version_str, text=text)


@app.route('/submit', methods=['POST'])
def search():
    form = SearchForm()
    form.validate_on_submit()
    return index(query=form.qfield.data)

#route index
@app.route('/', methods=['GET'])
def index(query=''):
    data = {
        "title": "Hello World",
        "body": "Flask simple MVC"
    }
    form = SearchForm()
    form.validate_on_submit()
    
    hotel_list = app.data_hotel_list
    tf_dict = app.data_tf_dict

    print("QUERY: {}".format(query))

    location = ''
    matched_hotels = parse_location(hotel_list, location)
    data = []
    for obj in matched_hotels:
        score = cal_final_score(obj, query, tf_dict)
        data.append((score, obj))
    data.sort(key=lambda x: x[0], reverse=True)


    # data = []
    # for h in hotel_list:
    #     score = rank_aspect(h, query)
    #     packed_data = (score, h)
    #     data.append(packed_data)

    # data.sort(key=lambda x: x[0], reverse=True)

    # print(data[:5])

    version_str = get_version_string()

    return render_template('index.html.j2', vers=version_str, form=form, hotels=data)
