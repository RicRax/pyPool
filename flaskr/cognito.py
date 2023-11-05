from os import access
from flask import (
    Flask,
    make_response,
    redirect,
    render_template,
    request,
    jsonify,
    url_for,
)
from flask_awscognito import AWSCognitoAuthentication
from jwt.algorithms import RSAAlgorithm
import requests
import jwt
import json
from flask_jwt_extended import (
    JWTManager,
    get_jwt,
    set_access_cookies,
    verify_jwt_in_request,
    get_jwt_identity,
)

from . import db


def get_cognito_public_keys():
    region = "eu-central-1"
    pool_id = "eu-central-1_a2CTG8CYM"
    url = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"

    resp = requests.get(url)
    return json.dumps(json.loads(resp.text)["keys"][1])


def cognitoRoutes(app, aws_auth):
    jwtManager = JWTManager(app)
    app.config["JWT_PUBLIC_KEY"] = RSAAlgorithm.from_jwk(get_cognito_public_keys())

    @app.route("/sign_in")
    def sign_in():
        return redirect(aws_auth.get_sign_in_url())

    @app.route("/aws_cognito_redirect")
    def aws_cognito_redirect():
        access_token = aws_auth.get_access_token(request.args)
        resp = make_response(redirect(url_for("home")))
        set_access_cookies(resp, access_token, max_age=30 * 60)
        return resp

    @app.route("/home")
    def home():
        verify_jwt_in_request()
        if get_jwt_identity():
            id = get_jwt()
            if db.checkIfUserExists(id["username"].strip("'"), id["sub"]):
                polls = db.getPollsOfUser(id["username"])
            else:
                polls = None
                db.addUser(id["username"], id["sub"])

            return render_template("home.html", username=id["username"], polls=polls)
        else:
            return redirect(aws_auth.get_sign_in_url())
