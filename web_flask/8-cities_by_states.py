#!/usr/bin/python3
"""
Starts a Flask web application to display states and cities
"""

from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Render an HTML page listing states with their cities

    Fetches all State instances from the storage, each with its associated
    cities. The states and cities are displayed in alphabetical order within
    the template.

    Returns:
        str: Rendered HTML page displaying states and their cities
    """
    # Retrieve all State objects from storage
    states = storage.all("State").values()
    # Render the template with the states and their cities
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage session at the end of the request

    Ensures that the storage (database) connection is closed properly after
    each request. This is done regardless of whether an exception occurred 
    during request handling.

    Args:
        exception (Exception): Exception object if an exception was raised during request handling
    """
    storage.close()


if __name__ == '__main__':
    # Run the Flask web application on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000)
