from flask import Flask, redirect, request, jsonify
from flask_awscognito import AWSCognitoAuthentication


def cognitoRoutes(app, aws_auth):
    @app.route("/sign_in")
    def sign_in():
        return redirect(aws_auth.get_sign_in_url())

    @app.route("/aws_cognito_redirect")
    def aws_cognito_redirect():
        access_token = aws_auth.get_access_token(request.args)
        return jsonify({"access_token": access_token})
