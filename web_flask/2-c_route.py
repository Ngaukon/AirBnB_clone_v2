#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def index():
    """Returns a greeting message 'Hello HBNB!'"""
    return 'Hello HBNB!'

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Returns a message 'HBNB'"""
    return 'HBNB'

@app.route('/c/<text>', strict_slashes=False)
def cisfun(text):
    """Returns 'C ' followed by the value of the text variable
    
    Replaces underscores in the text variable with spaces.

    Args:
        text (str): The text to display after 'C '
    
    Returns:
        str: The formatted string with 'C ' followed by the processed text
    """
    return 'C ' + text.replace('_', ' ')

if __name__ == '__main__':
    # Run the Flask application on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000)
