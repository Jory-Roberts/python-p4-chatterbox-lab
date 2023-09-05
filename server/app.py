from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def home():
    return "<h1>GET-POST-PATCH-DELETE-LAB</h1>"


@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.order_by("created_at").all()

        response = make_response(
            jsonify([message.to_dict() for message in messages]), 200
        )

    elif request.method == "POST":
        message_data = request.get_json()
        message = Message(body=message_data["body"], username=message_data["username"])

        db.session.add(message)
        db.session.commit()

        response = make_response(jsonify(message.to_dict()), 201)

    return response


@app.route("/messages/<int:id>", methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == "PATCH":
        message_data = request.get_json()
        for attr in message_data:
            setattr(message, attr, message_data[attr])

        db.session.add(message)
        db.session.commit()

        response = make_response(jsonify(message.to_dict()), 200)

    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()

        response = make_response(jsonify({"deleted": True}), 200)

    return response


if __name__ == "__main__":
    app.run(port=5555)
