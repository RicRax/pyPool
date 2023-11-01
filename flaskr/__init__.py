import os
from types import MethodType

from flask import Flask, app, request, redirect, jsonify, url_for
from flask_awscognito import AWSCognitoAuthentication
from dotenv import load_dotenv
import logging

from .config import Config
from . import cognito
from . import db
from . import polls


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.debug = True

    load_dotenv()

    aws_auth = AWSCognitoAuthentication(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    app.logger.addHandler(console_handler)

    cognito.cognitoRoutes(app, aws_auth)
    polls.createPollRoutes(app, aws_auth)
    db.initDB(app)

    return app
