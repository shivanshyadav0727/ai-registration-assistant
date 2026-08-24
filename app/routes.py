from flask import Blueprint, render_template, request, jsonify
from dialog.assistant import RegistrationAssistant

main = Blueprint("main", __name__)

assistant = RegistrationAssistant()


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/api/start", methods=["POST"])
def start():
    return jsonify({
        "response": assistant.start(),
        "state": assistant.get_state()
    })


@main.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    response = assistant.process(message)

    return jsonify({
        "response": response,
        "state": assistant.get_state(),
        "data": assistant.get_data()
    })