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
import logging
from flask_jwt_extended import (
    get_jwt,
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
        verify_jwt_in_request()
        if get_jwt_identity() is None:
            return jsonify({"claims": "not authenticated"})
        else:
            id = get_jwt()
        app.logger.info(f"Received form data: {request.get_json()}")
        data = request.get_json()
        db.createPoll(
            data["poll_title"],
            data["poll_description"],
            data["choices[]"],
            id["username"],
        )
        return jsonify("hello")

    @app.route("/getpoll/<int:pollid>")
    def getpoll(pollid):
        # verify_jwt_in_request()
        # if get_jwt_identity() is none:
        #     return jsonify({"claims": "not authenticated"})
        #
        pollinfo = db.selectPoll(pollid)

        print(pollinfo)

        return jsonify(pollinfo)

    @app.route("/viewPoll/<pollTitle>")
    def viewPoll(pollTitle):
        verify_jwt_in_request()
        if get_jwt_identity() is None:
            return jsonify({"claims": "not authenticated"})
        pollID = db.getPollIdFromTitle(pollTitle)
        return render_template("viewPoll.html", pollID=pollID)

    @app.route("/votePoll/<int:pollID>")
    def votePoll(pollID):
        verify_jwt_in_request()
        if get_jwt_identity() is None:
            return jsonify({"claims": "not authenticated"})
        return render_template("votePoll.html", pollID=pollID)

    @app.route("/voteEndpoint/<int:pollID>", methods=["POST"])
    def voteEndpoint(pollID):
        verify_jwt_in_request()
        if get_jwt_identity() is None:
            return jsonify({"claims": "not authenticated"})

        data = request.get_json()

        choiceText = data["choice"]

        votes = db.insertVote(pollID, choiceText)
        print(votes)
        return jsonify(votes)

    @app.route("/getChoicesText/<int:pollid>")
    def getChoicesText(pollid):
        # verify_jwt_in_request()
        # if get_jwt_identity() is none:
        #     return jsonify({"claims": "not authenticated"})
        #
        choices = db.getChoicesText(pollid)

        print(choices)

        return jsonify(choices)

    @app.route("/getChoices/<int:pollid>")
    def getChoices(pollid):
        # verify_jwt_in_request()
        # if get_jwt_identity() is none:
        #     return jsonify({"claims": "not authenticated"})
        #
        choices = db.getChoices(pollid)

        print(choices)

        return jsonify(choices)
