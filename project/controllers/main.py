"""
    Example Controllers
"""

from flask import render_template

from project import app
from project.models.SearchForm import SearchForm
from project.controllers.QueryProcess import parse_location, cal_final_score, load_single_review_tf

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
    return index(query=form.qfield.data, location=form.lfield.data)

#route index
@app.route('/', methods=['GET'])
def index(query='', location=''):
    form = SearchForm()
    form.validate_on_submit()
    
    data = {
        "title": "Hello World",
        "body": "Flask simple MVC"
    }
    form = SearchForm()
    form.validate_on_submit()
    
    hotel_list = app.data_hotel_list
    tf_dict = app.data_tf_dict

    print("QUERY: {}".format(query))
    print("LOCATION: {}".format(location))

    matched_hotels = parse_location(hotel_list, location)
    data = []
    for obj in matched_hotels:
        single_review_tf = load_single_review_tf(obj.id)
        score = cal_final_score(obj, query, single_review_tf)
        data.append((score, obj))
    data.sort(key=lambda x: x[0], reverse=True)

    version_str = get_version_string()

    return render_template('index.html.j2', vers=version_str, form=form, hotels=data)
