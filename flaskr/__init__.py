import os
from types import MethodType

from flask import Flask, app, request, redirect, jsonify, url_for
from flask_awscognito import AWSCognitoAuthentication

from .config import Config
from . import cognito


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    aws_auth = AWSCognitoAuthentication(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    cognito.cognitoRoutes(app, aws_auth)

    @app.route("/index")
    @aws_auth.authentication_required
    def hello():
        claims = aws_auth.claims
        return jsonify({"claims": claims})

    return app
