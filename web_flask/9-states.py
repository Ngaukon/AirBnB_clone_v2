#!/usr/bin/python3
"""
Starts a Flask web application to display states and their cities.
"""

from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def states(state_id=None):
    """Render an HTML page with a list of states and their cities

    If a specific state_id is provided, only that state's details will be displayed.

    Args:
        state_id (str, optional): The ID of a specific state to filter by. Defaults to None.

    Returns:
        str: Rendered HTML page displaying states and their cities
    """
    # Retrieve all State objects from storage
    states = storage.all("State")
    
    # If a specific state_id is provided, format it for lookup
    if state_id is not None:
        state_id = 'State.' + state_id
    
    # Render the template with the states and, if applicable, the specific state_id
    return render_template('9-states.html', states=states, state_id=state_id)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage session at the end of the request

    Ensures that the storage (database) connection is properly closed after 
    each request, regardless of whether an exception was raised during handling.

    Args:
        exception (Exception): Exception object if an exception occurred during request handling
    """
    storage.close()


if __name__ == '__main__':
    # Run the Flask web application on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000)
