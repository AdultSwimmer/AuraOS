from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import hashlib
import webbrowser
import threading

app = Flask(__name__)
CORS(app)

BASE_DIR = "users"
os.makedirs(BASE_DIR, exist_ok=True)



app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/favicon.ico")
def favicon():
    return "", 204



# =========================
# ID SYSTEM (HISTORY.TXT SEED)
# =========================
def make_user_id(first, last, username):
    raw = f"{first}:{last}:{username}".lower().strip()
    return hashlib.sha256(raw.encode()).hexdigest()

def user_folder(uid):
    return os.path.join(BASE_DIR, uid)

def memory_path(uid):
    return os.path.join(user_folder(uid), "memory.json")

def load_memory(uid):
    try:
        path = memory_path(uid)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except:
        return {}

def save_memory(uid, data):
    os.makedirs(user_folder(uid), exist_ok=True)
    with open(memory_path(uid), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# =========================
# SERVE HTML UI
# =========================
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# =========================
# RESTORE FROM HISTORY.TXT
# =========================
@app.route("/restore", methods=["POST"])
def restore():
    data = request.json

    first = data.get("first", "")
    last = data.get("last", "")
    username = data.get("username", "")
    memory = data.get("memory", {})

    uid = make_user_id(first, last, username)

    save_memory(uid, memory)

    return jsonify({
        "user_id": uid,
        "memory": memory
    })

# =========================
# CHAT ENDPOINT
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    uid = data["user_id"]
    message = data.get("message", "")

    mem = load_memory(uid)
    mem.setdefault("messages", []).append(message)

    reply = f"Aura: {message}"

    mem["last_reply"] = reply

    save_memory(uid, mem)

    return jsonify({
        "reply": reply
    })

# =========================
# AUTO OPEN UI
# =========================
def open_browser():
    webbrowser.open("http://127.0.0.1:8000")

# =========================
# START SERVER (LOCAL ONLY)
# =========================
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False,
        use_reloader=False
    )