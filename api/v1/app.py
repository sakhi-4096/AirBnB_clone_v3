#!/usr/bin/python3
"""Flask Application
This script creates a Flask application with the following features:
- Registers the app_views blueprint from api.v1.views
- Implements a method to handle app.teardown_appcontext, which calls storage.close()
- Runs the Flask server with configurable host and port values.
"""

from api.v1.views import app_views
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from models import storage
from os import environ


# Define default values for host and port
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = '5000'

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """Close Database Connection
    This function is called when the application context is torn down, and it
    ensures that
    the database connection is closed properly.
    Args:
        error: An error, if any, that occurred during the app context teardown.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Error.
    Returns a JSON response indicating that the requested resource was not found.
    """
    return make_response(jsonify({'error': "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)

if __name__ == "__main__":
    # Get host and port from environment variables or use defaults
    host = environ.get('HBNB_API_HOST', DEFAULT_HOST)
    port = environ.get('HBNB_API_PORT', DEFAULT_PORT)

    app.run(host=host, port=port, threaded=True)
