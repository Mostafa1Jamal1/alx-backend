#!/usr/bin/env python3
"""Flask app for learing I18n
"""

from flask import (
    Flask,
    render_template,
    request,
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


@babel.localeselector
def get_locale():
    """ to determine the best match with our supported languages.
    """
    if request.args.get('locale') is not None:
        return request.args.get('locale')
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/")
@app.route("/<lang>")
def hello_world():
    """home route for a basic page
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run()
