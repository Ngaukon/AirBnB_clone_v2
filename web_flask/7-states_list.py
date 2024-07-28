#!/usr/bin/python3
"""
Starts a Flask web application to display a list of states
"""

from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Render an HTML page with a list of states sorted in alphabetical order

    Fetches all State instances from the storage, sorts them by name, and
    passes them to the template for rendering.

    Returns:
        str: Rendered HTML page displaying the list of states
    """
    # Retrieve all State objects from storage and sort them by name
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    # Render the template with the sorted states list
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage session at the end of the request

    Ensures that the storage (database) connection is closed properly after
    each request, regardless of whether an exception occurred.

    Args:
        exception (Exception): Exception object if an exception was raised during request handling
    """
    storage.close()


if __name__ == '__main__':
    # Run the Flask web application on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000)

