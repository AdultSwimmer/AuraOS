from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, hashlib

app = Flask(__name__)
CORS(app)

BASE = "users"
os.makedirs(BASE, exist_ok=True)

# =========================
# ID FROM HISTORY FILE
# =========================
def make_id(first, last, username):
    raw = f"{first}:{last}:{username}".lower().strip()
    return hashlib.sha256(raw.encode()).hexdigest()

def path(uid):
    return os.path.join(BASE, uid)

def memory(uid):
    file = os.path.join(path(uid), "memory.json")
    if os.path.exists(file):
        return json.load(open(file, "r", encoding="utf-8"))
    return {}

def save(uid, data):
    os.makedirs(path(uid), exist_ok=True)
    with open(os.path.join(path(uid), "memory.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# =========================
# LOGIN / RESTORE FROM HISTORY
# =========================
@app.route("/restore", methods=["POST"])
def restore():
    data = request.json

    # From uploaded HISTORY file (already parsed in HTML)
    uid = make_id(
        data.get("first",""),
        data.get("last",""),
        data.get("username","")
    )

    mem = data.get("memory", {})

    save(uid, mem)

    return jsonify({
        "user_id": uid,
        "memory": mem
    })

# =========================
# CHAT
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    uid = data["user_id"]
    msg = data.get("message","")

    mem = memory(uid)

    mem.setdefault("messages", []).append(msg)

    reply = f"Aura: I remember you said '{msg}'"

    mem["last_reply"] = reply

    save(uid, mem)

    return jsonify({
        "reply": reply
    })

# =========================
# START
# =========================
if __name__ == "__main__":
    print("AuraOS running on http://localhost:8000")
    app.run(host="0.0.0.0", port=8000)