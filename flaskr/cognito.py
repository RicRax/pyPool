from os import access
from flask import Flask, make_response, redirect, request, jsonify, url_for
from flask_awscognito import AWSCognitoAuthentication
from jwt.algorithms import RSAAlgorithm
import json
import requests
from flask_jwt_extended import (
    JWTManager,
    set_access_cookies,
    verify_jwt_in_request,
    get_jwt_identity,
)


def get_cognito_public_keys():
    region = "eu-central-1"
    pool_id = "eu-central-1_a2CTG8CYM"
    url = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"

    resp = requests.get(url)
    return json.dumps(json.loads(resp.text)["keys"][1])


def cognitoRoutes(app, aws_auth):
    jwt = JWTManager(app)
    app.config["JWT_PUBLIC_KEY"] = RSAAlgorithm.from_jwk(get_cognito_public_keys())

    @app.route("/sign_in")
    def sign_in():
        return redirect(aws_auth.get_sign_in_url())

    @app.route("/aws_cognito_redirect")
    def aws_cognito_redirect():
        access_token = aws_auth.get_access_token(request.args)
        resp = make_response(redirect(url_for("protected")))
        set_access_cookies(resp, access_token, max_age=30 * 60)
        return resp

    @app.route("/protected")
    def protected():
        verify_jwt_in_request()
        if get_jwt_identity():
            return jsonify({"claims": "it works"})
        else:
            return redirect(aws_auth.get_sign_in_url())
