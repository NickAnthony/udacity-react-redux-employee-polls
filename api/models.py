import os
from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import datetime
import string
import random

database_path = os.environ.get("DATABASE_URL")
if not database_path:
    database_path = "postgresql://localhost:5432/employeepolls"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """setup_db(app)

    Binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.app_context().push()
    migrate = Migrate(app, db)


def generate_random_id():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=64))


class GeneralModel:
    def insert(self):
        """Inserts a new model into the database

        The model must have a unique id or null id
        EXAMPLE:
            model = Model(req_param=req_param)
            model.insert()
        """
        exception = None
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise (e)

    def delete(self):
        """Deletes an existing model from the database

        The model must exist in the database
        EXAMPLE
            model = Model.query.first()
            model.delete()
        """
        exception = None
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise (e)

    def update(self):
        """Updates an existing model in the database

        the model must exist in the database
        EXAMPLE
            model = Model.query.first()
            model.my_number = 41
            model.update()
        """
        exception = None
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise (e)


class User(db.Model, GeneralModel):
    """User

    Represents a user.
    """

    __tablename__ = "users"

    id = Column(String(64), primary_key=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)

    # One to many relationship with questions
    questions = db.relationship("Question", backref=db.backref("author", lazy="joined"))

    # Has one to many relationship with answers, with backref `user`
    answers = db.relationship("Answer", backref=db.backref("user", lazy="joined"))

    def __init__(self, id, password, name, avatar_url=None):
        self.id = id
        self.name = name
        self.password = password
        self.avatar_url = avatar_url

    def format(self):
        formatted_questions = [question.id for question in self.questions]
        formatted_answers = [
            (answer.question_id, answer.vote) for answer in self.answers
        ]
        return {
            "id": self.id,
            "name": self.name,
            "avatar_url": self.avatar_url,
            "questions": formatted_questions,
            "answers": formatted_answers,
        }

    def __repr__(self):
        return f"<User {self.id} {self.name}>"


class Question(db.Model, GeneralModel):
    """Question

    Represents a question with two options.
    """

    __tablename__ = "questions"

    id = Column(String(64), primary_key=True)
    optionOne = Column(String, nullable=False)
    optionTwo = Column(String, nullable=False)
    timestamp = Column(BigInteger, nullable=False)

    # Has one to many relationship with users, with backref `author`
    author_id = Column(String, ForeignKey("users.id"))

    # Has one to many relationship with answers, with backref `question`
    answers = relationship("Answer", backref=db.backref("question", lazy="joined"))

    def __init__(self, optionOne, optionTwo, id=None, timestamp=None):
        self.id = id if (id != None) else generate_random_id()
        self.optionOne = optionOne
        self.optionTwo = optionTwo
        self.timestamp = (
            timestamp if (timestamp != None) else datetime.datetime.now().timestamp()
        )

    def format(self):
        optionOneVotes = []
        optionTwoVotes = []
        for answer in self.answers:
            if answer.vote == 1:
                optionOneVotes.append(answer.author_id)
            if answer.vote == 2:
                optionTwoVotes.append(answer.author_id)

        return {
            "id": self.id,
            "question": self.question,
            "optionOne": self.optionOne,
            "optionTwo": self.optionTwo,
            "timestamp": self.timestamp,
            "author": self.author_id,
            "optionOneVotes": optionOneVotes,
            "optionTwoVotes": optionTwoVotes,
        }

    def __repr__(self):
        return f"<Question {self.id} {self.optionOne} {self.optionTwo}>"


class Answer(db.Model, GeneralModel):
    """Answer

    Represents a question answer.
    """

    __tablename__ = "answers"

    vote = Column(Integer, nullable=False)

    # Has one to many relationship with users, with backref `question`
    question_id = Column(String(64), ForeignKey("questions.id"), primary_key=True)

    # Has one to many relationship with users, with backref `user`
    user_id = Column(String(64), ForeignKey("users.id"), primary_key=True)

    def __init__(self, vote):
        self.vote = vote

    def format(self):
        return {
            "id": self.id,
            "questionId": self.question_id,
            "authorId": self.author_id,
            "vote": self.vote,
        }

    def __repr__(self):
        return f"<Answer {self.question_id} {self.author_id} {self.vote}>"


# setup_db(app)

# newUser = User(id="nickanthony", password="secret",
#                name="Nick Anthony", avatar_url="https://i.redd.it/ofmlty7h86fa1.jpg")

# newQuestion = Question(optionOne="have code reviews conducted by peers",
#                        optionTwo="have code reviews conducted by managers")
# newQuestion.author = newUser

# newAnswer = Answer(vote=1)
# newAnswer.user = newUser
# newAnswer.question = newQuestion

# newUser.insert()
# newQuestion.insert()
# newAnswer.insert()