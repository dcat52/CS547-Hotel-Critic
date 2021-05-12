#Project Flask MVC

__author__ = "WPI_Students"
__version__ = "0.5.1"
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

    except:
        h = Hotel()
        h.id = "0"
        h.name = "error"
        h.address = "error"

        hotel_list = [h]

    app.data_hotel_list = hotel_list

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    app.__version__ = __version__

    print("Running the app now.")
    app.run(host='0.0.0.0', port=8000, debug=False)
