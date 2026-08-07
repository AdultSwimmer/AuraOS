from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_DIR = os.path.join(BASE_DIR, "users")
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")

os.makedirs(USERS_DIR, exist_ok=True)
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)


# =========================
# LOAD KNOWLEDGE FILES
# =========================
def load_knowledge():
    data = {}

    if os.path.exists(KNOWLEDGE_DIR):
        for file in os.listdir(KNOWLEDGE_DIR):
            if file.endswith(".txt"):
                with open(os.path.join(KNOWLEDGE_DIR, file), "r", encoding="utf-8") as f:
                    data[file] = f.read()

    return data


knowledge_base = load_knowledge()


# =========================
# FRONTEND
# =========================
@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/favicon.ico")
def favicon():
    return "", 204


# =========================
# CHAT
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}

    message = data.get("message", "")
    user_id = data.get("user_id", "guest")

    return jsonify({
        "reply": f"Aura: {message}",
        "knowledge": knowledge_base
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False,
        use_reloader=False
    )