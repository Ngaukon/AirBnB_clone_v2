#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)

@app.route('/hbnb_filters', strict_slashes=False)
def filters():
    """
    Displays an HTML page similar to 6-index.html, populated with data from
    the storage engine.

    The page will include a list of all states and amenities available 
    in the application, fetched from the storage.
    """
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)

@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the storage connection after each request.

    This ensures that the database connection is properly closed 
    after the app context is torn down.
    """
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
