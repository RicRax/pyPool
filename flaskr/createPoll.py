from flask import (
    Flask,
    make_response,
    redirect,
    render_template,
    request,
    jsonify,
    url_for,
)
import json
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity,
)

from . import db


def createPollRoutes(app, aws_auth):
    @app.route("/createPoll")
    def createPoll():
        verify_jwt_in_request()
        if get_jwt_identity() is None:
            return jsonify({"claims": "not authenticated"})
        return render_template("createPoll.html")

    @app.route("/createEndpoint", methods=["POST"])
    def createEndpoint():
        db.createPoll(request.form["poll_title"], request.form["poll_description"])

        return jsonify(request.form)
