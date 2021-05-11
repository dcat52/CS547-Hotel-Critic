#Project Flask MVC

__author__ = "WPI_Students"
__version__ = "0.2.3"
__email__ = "_@wpi.edu"

from project import app
from flask_bootstrap import Bootstrap
from project.models.Hotel import Hotel
import pickle
import os.path

if __name__ == '__main__':
    Bootstrap(app)

    app.debug = True

    
    try:
        fn = '/home/site/wwwroot/hotel_list.pkl'
        if not os.path.isfile(fn):
            fn = 'hotel_list.pkl'

        with open(fn, 'rb') as handle:
            hotel_list = pickle.load(handle)

        fn = '/home/site/wwwroot/review_tf.pkl'
        if not os.path.isfile(fn):
            fn = 'review_tf.pkl'
        with open(fn, 'rb') as handle:
            tf_dict = pickle.load(handle)

    except:
        h = Hotel()
        h.id = "0"
        h.name = "error"
        h.address = "error"

        hotel_list = [h]
        tf_dict = {"0":{'error':1}}
        # with open('hotel_list.pkl', 'rb') as handle:
        #     hotel_list = pickle.load(handle)

        # with open('review_tf.pkl', 'rb') as handle:
        #     tf_dict = pickle.load(handle)

    # tf_dict = {}

    app.data_hotel_list = hotel_list
    app.data_tf_dict = tf_dict

    # # attempt to get data from home directory
    # app.bt = binarytree.binary_tree()
    # app.hotels = []
    # app.data = build_hotel_obj_data('/home/json_small/*.json')
    
    # # if failed, get the data local directory
    # if len(app.data) == 0:
    #     app.data = build_hotel_obj_data('./json_small/*.json')

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    app.__version__ = __version__

    print("Running the app now.")
    app.run(host='0.0.0.0', port=8000, debug=True)
