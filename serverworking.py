from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

import os
import json
import hashlib
import requests
import sys
from datetime import datetime, timezone

# =========================
# FLASK
# =========================
app = Flask(__name__)
CORS(app)

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_DIR = os.path.join(BASE_DIR, "users")
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
CORE_DIR = os.path.join(BASE_DIR, "core")

CORE_FILE = os.path.join(CORE_DIR, "core.txt")

MANIFEST_URL = "http://127.0.0.1:5050/manifest.json"

os.makedirs(USERS_DIR, exist_ok=True)
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
os.makedirs(CORE_DIR, exist_ok=True)

# =========================
# TIME SYSTEM
# =========================
def now():
    return datetime.now(timezone.utc).isoformat()

# =========================
# HASH SYSTEM
# =========================
def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# =========================
# REMOTE INTEGRITY CHECK
# =========================
def validate_remote():

    print("Checking integrity...")

    try:
        response = requests.get(MANIFEST_URL, timeout=5)
        manifest = response.json()

    except Exception as e:
        print("FAILED TO CONTACT AUTHORITY SERVER")
        print(str(e))
        sys.exit(1)

    for file_path, expected_hash in manifest.items():

        # USER MEMORY FILES ARE ALLOWED TO CHANGE
        if "HISTORY.txt" in file_path:
            continue

        local_path = os.path.join(BASE_DIR, file_path)

        if not os.path.exists(local_path):
            print(f"MISSING FILE: {file_path}")
            sys.exit(1)

        actual_hash = file_hash(local_path)

        if actual_hash != expected_hash:
            print(f"TAMPER DETECTED: {file_path}")
            sys.exit(1)

    print("Integrity verified.")

# =========================
# LOAD CORE FILE
# =========================
def load_core():

    if not os.path.exists(CORE_FILE):
        print("core.txt missing.")
        sys.exit(1)

    with open(CORE_FILE, "r", encoding="utf-8") as f:
        return f.read()

# =========================
# LOAD KNOWLEDGE FILES
# =========================
def load_knowledge():

    data = {}

    if os.path.exists(KNOWLEDGE_DIR):

        for file in os.listdir(KNOWLEDGE_DIR):

            if file.endswith(".txt"):

                path = os.path.join(KNOWLEDGE_DIR, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data[file] = f.read()

                except Exception as e:
                    print(f"FAILED TO LOAD {file}")
                    print(str(e))

    return data

# =========================
# SYSTEM BOOT
# =========================
print("===================================")
print("AURA SYSTEM START")
print("===================================")

validate_remote()

CORE_MEMORY = load_core()

knowledge_base = load_knowledge()

print(f"Loaded knowledge files: {len(knowledge_base)}")

print("SYSTEM READY")
print("===================================")

# =========================
# FRONTEND
# =========================
@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

# =========================
# FAVICON FIX
# =========================
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

    event = {
        "type": "message",
        "text": message,
        "time": now()
    }

    reply = {
        "text": f"Aura: {message}",
        "time": now()
    }

    return jsonify({
        "reply": reply,
        "event": event,
        "core_loaded": True,
        "knowledge_files": len(knowledge_base)
    })

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False,
        use_reloader=False
    )