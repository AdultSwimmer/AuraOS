"""
AuraOS Server — minimal persistent-memory harness
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from datetime import datetime, timezone

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
CORE_DIR = os.path.join(ROOT_DIR, "core")
HISTORY_DIR = os.path.join(ROOT_DIR, "histories")

os.makedirs(HISTORY_DIR, exist_ok=True)

# --------------- Config ---------------
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
MODEL = os.getenv("AURA_MODEL", "dolphin3:8b")
HOST = os.getenv("AURA_HOST", "0.0.0.0")
PORT = int(os.getenv("AURA_PORT", "8000"))


def now():
    return datetime.now(timezone.utc).isoformat()


def load_core():
    """Load every text file in core/ as permanent identity."""
    if not os.path.exists(CORE_DIR):
        return "No core identity loaded."

    chunks = []
    for name in sorted(os.listdir(CORE_DIR)):
        if name.endswith((".txt", ".md")):
            path = os.path.join(CORE_DIR, name)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                chunks.append(f"[CORE: {name}]\n{content}")

    return "\n\n".join(chunks) if chunks else "No core identity loaded."


def load_history(user_id: str) -> str:
    path = os.path.join(HISTORY_DIR, f"{user_id}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def append_history(user_id: str, role: str, text: str):
    path = os.path.join(HISTORY_DIR, f"{user_id}.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{now()}] {role.upper()}\n{text}\n\n")


CORE_MEMORY = load_core()


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    message = data.get("message", "").strip()
    user_id = data.get("user_id", "default")

    if not message:
        return jsonify({"error": "Empty message"}), 400

    history = load_history(user_id)

    prompt = f"""=== CORE IDENTITY (permanent) ===
{CORE_MEMORY}

=== HISTORY ===
{history if history else "(no prior history)"}

=== CURRENT MESSAGE ===
User: {message}
Aura:"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        reply = response.json().get("response", "").strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Persist both sides
    append_history(user_id, "user", message)
    append_history(user_id, "aura", reply)

    return jsonify({
        "reply": reply,
        "user_id": user_id,
        "timestamp": now(),
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model": MODEL,
        "core_loaded": bool(CORE_MEMORY),
    })


if __name__ == "__main__":
    print("AuraOS harness starting...")
    print(f"Model: {MODEL}")
    print(f"Core identity characters: {len(CORE_MEMORY)}")
    app.run(host=HOST, port=PORT, debug=False)
