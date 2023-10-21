import os


class Config:
    DEBUG = True
    SECRET_KEY = "dev"
    AWS_DEFAULT_REGION = "eu-central-1"
    AWS_COGNITO_DOMAIN = "https://pypoll.auth.eu-central-1.amazoncognito.com"
    AWS_COGNITO_USER_POOL_ID = "eu-central-1_a2CTG8CYM"
    AWS_COGNITO_USER_POOL_CLIENT_ID = "3outcd9iasjelfcnr3m6c60ame"
    AWS_COGNITO_REDIRECT_URL = "http://localhost:5000/aws_cognito_redirect"
    AWS_COGNITO_USER_POOL_CLIENT_SECRET = (
        "10gbdtl519cp0fk2h5me2sveu6f375fbuc3eoo73l7o26nrvtotg"
    )

    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = True

    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ALGORITHM = "RS256"
    JWT_IDENTITY_CLAIM = "sub"

    SECRET_KEY = "abc"
    JWT_PRIVATE_KEY = "abc"
    JWT_ACCESS_COOKIE_NAME = "accessToken"
    JWT_COOKIE_DOMAIN = "localhost"
    JWT_ACCESS_COOKIE_PATH = "/"
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-Token"
    JWT_ACCESS_CSRF_FIELD_NAME = "csrf_token"

    # not used with cognito
    JWT_SECRET_KEY = "abc"
