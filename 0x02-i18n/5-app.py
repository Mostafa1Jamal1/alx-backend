#!/usr/bin/env python3
"""Flask app for learing I18n
"""

from flask import (
    Flask,
    render_template,
    request,
    g,
)
from flask_babel import Babel, _


class Config:
    """config class for babel
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """returns a user dictionary
    """
    log_as = request.args.get('login_as')
    if log_as is not None:
        log_as = int(log_as)
    return users.get(log_as)


@app.before_request
def before_request():
    """set user as a global on flask.g.user
    """
    if get_user() is not None:
        g.user = get_user()


@babel.localeselector
def get_locale():
    """ to determine the best match with our supported languages.
    """
    if request.args.get('locale') is not None:
        return request.args.get('locale')
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/")
@app.route("/<lang>")
@app.route("/<login_as>")
def hello_world():
    """home route for a basic page
    """
    return render_template('5-index.html')
