import os
from types import MethodType

from flask import Flask, app, request, redirect, jsonify, url_for
from flask_awscognito import AWSCognitoAuthentication
import logging

from .config import Config
from . import cognito
from . import db
from . import polls


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.debug = True

    aws_auth = AWSCognitoAuthentication(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.logger.setLevel(logging.DEBUG)

    # Create a logging handler for the console (terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Adjust the level as needed

    # Create a logging formatter to define how log messages are displayed
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    # Add the console handler to the app's logger
    app.logger.addHandler(console_handler)

    cognito.cognitoRoutes(app, aws_auth)
    polls.createPollRoutes(app, aws_auth)
    db.initDB(app)

    @app.route("/index")
    @aws_auth.authentication_required
    def hello():
        claims = aws_auth.claims
        return jsonify({"claims": claims})

    return app
