from flask import (
    render_template,
    request,
    jsonify,
)
from flask_jwt_extended import (
    get_jwt,
    verify_jwt_in_request,
    get_jwt_identity,
)

from . import db


def createPollRoutes(app, statsd):
    @app.route("/createPoll")
    def createPoll():
        verify_jwt_in_request()
        if get_jwt_identity() is None:
            return jsonify({"claims": "not authenticated"})
        return render_template("createPoll.html")

    @app.route("/polls", methods=["POST"])
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
        with statsd.timer("request.duration"):
            return jsonify("hello")

    @app.route("/polls/<int:pollid>")
    def getpoll(pollid):
        verify_jwt_in_request()
        if get_jwt_identity() is None:
            return jsonify({"claims": "not authenticated"})

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

    @app.route("/polls/<int:pollID>/vote", methods=["POST"])
    def voteEndpoint(pollID):
        verify_jwt_in_request()
        if get_jwt_identity() is None:
            return jsonify({"claims": "not authenticated"})

        data = request.get_json()

        choiceText = data["choice"]

        votes = db.insertVote(pollID, choiceText)
        print(votes)
        return jsonify(votes)

    @app.route("/choices/<int:pollid>/text")
    def getChoicesText(pollid):
        # verify_jwt_in_request()
        # if get_jwt_identity() is none:
        #     return jsonify({"claims": "not authenticated"})
        #
        choices = db.getChoicesText(pollid)

        print(choices)

        return jsonify(choices)

    @app.route("/choices/<int:pollid>")
    def getChoices(pollid):
        # verify_jwt_in_request()
        # if get_jwt_identity() is None:
        #     return jsonify({"claims": "not authenticated"})
        #
        choices = db.getChoices(pollid)

        print(choices)

        return jsonify(choices)

    @app.route("/polls/{pollTitle}")
    def deletePoll(pollTitle):
        verify_jwt_in_request()
        if get_jwt_identity() is None:
            return jsonify({"claims": "not authenticated"})

        db.deletePoll(pollTitle)

        return jsonify({"claims": "Poll {pollTitle} successfully deleted"})
