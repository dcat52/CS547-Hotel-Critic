#Project Flask MVC

__author__ = "WPI_Students"
__version__ = "0.2.3"
__email__ = "_@wpi.edu"

from project import app
from flask_bootstrap import Bootstrap

from project.models.Hotel import Hotel
from project.controllers.DataPreprocess import *
from project.controllers.QueryProcess import *

if __name__ == '__main__':
    Bootstrap(app)

    app.debug = True

    # attempt to get data from home directory
    app.data = build_data('/home/json_small/*.json')
    
    # if failed, get the data local directory
    if len(app.data) == 0:
        app.data = build_data('./json_small/*.json')

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    app.__version__ = __version__

    print("Running the app now.")
    app.run(host='0.0.0.0', port=8000, debug=True)
