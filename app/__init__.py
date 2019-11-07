"Main Flask App"
# pylint: disable=import-outside-toplevel
from logging import Logger
from typing import List

from flask import Flask, jsonify, abort, request


# Application Factory
# https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
def create_app(config_name: str) -> Flask:
    """Create the Flask application
    
    Args:
        config_name (str): Config name mapping to Config Class
    
    Returns:
        [Flask]: Flask Application
    """
    from app.config import config_by_name

    # Create the app
    app = Flask(__name__)

    # Log the current config name being used and setup app with the config
    app.logger.debug(f"CONFIG NAME: {config_name}")
    config = config_by_name[config_name]
    app.config.from_object(config)

    @app.route("/")
    def hello_world() -> str:  # pylint: disable=unused-variable

        return "Hello World!"

    return app
