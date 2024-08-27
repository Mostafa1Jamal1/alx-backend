#!/usr/bin/env python3
"""Flask app for learing I18n
"""

from flask import (
    Flask,
    render_template,
)


app = Flask(__name__)


@app.route("/")
def hello_world():
    """home route for a basic page
    """
    return render_template('0-index.html')
