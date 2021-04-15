#Project Flask MVC

__author__ = "WPI_Students"
__version__ = "0.2.2"
__email__ = "_@wpi.edu"

from project import app
from flask_bootstrap import Bootstrap

if __name__ == '__main__':
    Bootstrap(app)

    app.debug = True

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    app.__version__ = __version__

    app.run(host="localhost", port=8000, debug=True)
