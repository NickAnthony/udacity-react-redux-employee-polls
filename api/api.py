from flask import Flask, send_from_directory, jsonify, request, abort
from flask_cors import CORS  # comment this on deployment
from api.models import setup_db, User, Question, Answer, db
import sys


def create_app(test_config=None):
    app = Flask(__name__, static_url_path="", static_folder="../build")
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/", defaults={"path": ""})
    def index(path):
        return send_from_directory(app.static_folder, "index.html")

    # ----------------------------------------------------------------------- #
    # User endpoints/routes.
    # ----------------------------------------------------------------------- #

    """
    GET /users
        - A Public Endpoint that fetches a list of all users.
        - Permissions required: None
        - Request Arguments: None
        - Returns:
          - Status code 200 and json {"success": True, "users": users}
            where users is a list of all usernames.
    """

    @app.route("/users", methods=["GET"])
    def get_users():
        users = User.query.all()
        formatted_users = {}
        for user in users:
            formatted_users[user.id] = {
                "id": user.id,
                "name": user.name,
                "avatar_url": user.avatar_url,
                "answers": {},
                "questions": [question.id for question in user.questions],
            }
            for answer in user.answers:
                vote = "optionOne" if (answer.vote == 1) else "optionTwo"
                formatted_users[user.id]["answers"][answer.question_id] = vote

        return jsonify({"success": True, "users": formatted_users})

    """
    POST /users
        - Creates a new user and stores it in the database.  It will throw
            a 400 if the incorrect parameters are passed.
        - Permissions required: None
        - Request Arguments:
            - 'username': A unique string.
            - 'password': A password for the user.
            - 'name': A string that is the full name of the user.
            - 'avatar_url': A url pointing to a photo of the user.
        - Returns:
          - Status code 200 and json {"success": True}
    """

    @app.route("/users", methods=["POST"])
    def add_new_user():
        if not request.get_json():
            abort(400)
        id = request.get_json().get("username", None)
        password = request.get_json().get("password", None)
        name = request.get_json().get("name", None)
        avatar_url = request.get_json().get("avatar_url", None)

        # Verify that the appropriate parameters were passed.
        if not id or not password or not name:
            abort(400)

        # Verify that the provided username isn't taken
        users = User.query.all()
        for user in users:
            if user.id == id:
                abort(404)

        try:
            newUser = User(id, password, name, avatar_url)
            newUser.insert()
            return jsonify({"success": True, "id": newUser.id})
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    """
    POST /login
        - Checks a password for login.  Technically, this isn't a
            safe way to do this, but it's free.  For a production
            app I would recommend using OAuth.
        - Permissions required: None
        - Request Arguments:
            - 'username': A unique string.
            - 'password': A password for the user.
        - Returns:
          - Status code 200 and json {"success": True}
    """

    @app.route("/login", methods=["POST"])
    def login():
        if not request.get_json():
            abort(400)
        id = request.get_json().get("id", None)
        password = request.get_json().get("password", None)

        # Verify that the appropriate parameters were passed.
        if not id or not password:
            abort(400)

        # Verify that the user exists.
        user = User.query.filter(User.id == id).one_or_none()
        if not user:
            abort(404)

        if user.password == password:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})

    # ----------------------------------------------------------------------- #
    # Questions endpoints/routes.
    # ----------------------------------------------------------------------- #

    """
    GET /questions
        - A Public Endpoint that fetches a list of all questions.
        - Permissions required: None
        - Request Arguments: None
        - Returns:
          - Status code 200 and json {"success": True, "questions": questions}
            where question is a list of all questions.
    """

    @app.route("/questions", methods=["GET"])
    def get_questions():
        questions = Question.query.all()
        formatted_questions = {}

        for question in questions:
            formatted_questions[question.id] = {
                "id": question.id,
                "author": question.author_id,
                "timestamp": question.timestamp,
                "optionOne": {
                    "votes": [],
                    "text": question.optionOne,
                },
                "optionTwo": {
                    "votes": [],
                    "text": question.optionTwo,
                },
            }
            for answer in question.answers:
                if answer.vote == 1:
                    formatted_questions[question.id]["optionOne"]["votes"].append(
                        answer.user_id
                    )
                else:
                    formatted_questions[question.id]["optionTwo"]["votes"].append(
                        answer.user_id
                    )

        return jsonify({"success": True, "questions": formatted_questions})

    """
    POST /questions
        - A Public Endpoint saves a new question.
        - Permissions required: None
        - Request Arguments:
            - 'username': Author of the question.
            - 'optionOne': Option one of the question.
            - 'optionTwo': Option one of the question.
        - Returns:
          - Status code 200 and json {"success": True, "question": question}
            where question is the question saved.
    """

    @app.route("/questions", methods=["POST"])
    def add_new_question():
        if not request.get_json():
            abort(400)
        username = request.get_json().get("username", None)
        optionOne = request.get_json().get("optionOne", None)
        optionTwo = request.get_json().get("optionTwo", None)

        # Verify that the appropriate parameters were passed.
        if not username or not optionOne or not optionTwo:
            abort(400)

        # Verify that the user exists.
        author = User.query.filter(User.id == username).one_or_none()
        if not author:
            abort(404)

        try:
            newQuestion = Question(optionOne, optionTwo)
            newQuestion.author = author
            newQuestion.insert()
            return jsonify(
                {
                    "success": True,
                    "question": {
                        "id": newQuestion.id,
                        "author": newQuestion.author_id,
                        "timestamp": newQuestion.timestamp,
                        "optionOne": {
                            "votes": [],
                            "text": newQuestion.optionOne,
                        },
                        "optionTwo": {
                            "votes": [],
                            "text": newQuestion.optionTwo,
                        },
                    },
                }
            )
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    # ----------------------------------------------------------------------- #
    # Answer endpoints/routes.
    # ----------------------------------------------------------------------- #

    """
    POST /answers
        - A Public Endpoint saves a new answer.
        - Permissions required: None
        - Request Arguments:
            - 'vote': Vote 1 or 2 for answer.
            - 'username': Authed user answering the question.
            - 'question_id': Id of the question being answered..
        - Returns:
          - Status code 200 and json {"success": True}
    """

    @app.route("/answers", methods=["POST"])
    def add_new_answer():
        if not request.get_json():
            abort(400)
        vote = request.get_json().get("vote", None)
        username = request.get_json().get("username", None)
        question_id = request.get_json().get("question_id", None)

        # Verify that the appropriate parameters were passed.
        if not vote or not username or not question_id:
            abort(400)

        # Verify that the user exists.
        user = User.query.filter(User.id == username).one_or_none()
        if not user:
            abort(404)

        # Verify that the question exists.
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if not question:
            abort(404)

        try:
            newAnswer = Answer(vote)
            newAnswer.user = user
            newAnswer.question = question
            newAnswer.insert()
            return jsonify({"success": True})
        except Exception as e:
            print(sys.exc_info())
            abort(422)

    # ----------------------------------------------------------------------- #
    # Error handlers for all expected errors.
    # ----------------------------------------------------------------------- #
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {"success": False, "error": 404, "message": "Resource was not found"}
            ),
            404,
        )

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify(
                {"success": False, "error": 405, "message": "Method is not allowed"}
            ),
            405,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def unprocessable(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "Internal server error"}
            ),
            500,
        )

    return app
