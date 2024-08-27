#!/usr/bin/env python3
"""Flask app for learing I18n
"""

from flask import (
    Flask,
    render_template,
)
from flask_babel import Babel


class Config:
    """config class for babel
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@app.route("/")
def hello_world():
    """home route for a basic page
    """
    return render_template('1-index.html')
