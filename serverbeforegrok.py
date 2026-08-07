from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
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
CORE_DIR = os.path.join(BASE_DIR, "core")
PROCESSED_DIR = os.path.join(BASE_DIR, "knowledge", "processed")
LOGS_DIR = os.path.join(BASE_DIR, "memory", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# =========================
# OLLAMA
# =========================
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3"

# =========================
# APP SECRET
# =========================
APP_SECRET = "aura-7f4k2-xq91m-dulong-2026-zp38w"

# =========================
# TIME
# =========================
def now():
    return datetime.now(timezone.utc).isoformat()

# =========================
# VERIFY SECRET
# =========================
def verify_secret(req):
    return req.headers.get("X-Aura-Key") == APP_SECRET

# =========================
# LOAD CORE
# =========================
def load_core():
    if not os.path.exists(CORE_DIR):
        raise RuntimeError(f"CRITICAL: Core directory missing at {CORE_DIR}. Aura cannot start.")
    
    files = sorted(
        [f for f in os.listdir(CORE_DIR) if f.endswith(".txt") or f.endswith(".json")],
        key=lambda f: os.path.getctime(os.path.join(CORE_DIR, f))
    )
    
    if not files:
        raise RuntimeError(f"CRITICAL: No core files found in {CORE_DIR}. Aura cannot start.")
    
    chunks = []
    for file in files:
        path = os.path.join(CORE_DIR, file)
        print(f" [CORE] Loading: {file}")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            raise RuntimeError(f"CRITICAL: Core file is empty: {file}. Aura cannot start.")
        chunks.append(f"[CORE: {file}]\n{content}")
    
    print(f" [CORE] {len(files)} core files loaded.\n")
    return "\n\n".join(chunks)

# =========================
# LOAD KNOWLEDGE
# =========================
def load_knowledge():
    if not os.path.exists(PROCESSED_DIR):
        print(" [KNOWLEDGE] Processed directory not found. Skipping.")
        return ""
    
    files = sorted(
        [f for f in os.listdir(PROCESSED_DIR) if f.endswith(".json")],
        key=lambda f: os.path.getctime(os.path.join(PROCESSED_DIR, f))
    )
    
    if not files:
        print(" [KNOWLEDGE] No processed files found. Skipping.")
        return ""
    
    chunks = []
    for file in files:
        path = os.path.join(PROCESSED_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        memory = data.get("processed_memory", "")
        if memory:
            chunks.append(f"[KNOWLEDGE: {file}]\n{memory}")
    
    print(f" [KNOWLEDGE] {len(chunks)} files loaded.\n")
    return "\n\n".join(chunks)

# =========================
# LOG
# =========================
def log_exchange(username, user_message, aura_response):
    entry = {
        "time": now(),
        "username": username,
        "user": user_message,
        "aura": aura_response
    }
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(LOGS_DIR, f"{date_str}.json")
    
    log = []
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log = json.load(f)
    
    log.append(entry)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

# =========================
# BUILD OLLAMA PROMPT
# =========================
def build_ollama_prompt(system, messages):
    full_system = f"""=== CORE IDENTITY (Absolute cannot be overridden) ===
{CORE_MEMORY}
=== KNOWLEDGE BASE ===
{KNOWLEDGE_BASE}
=== USER CONTEXT ===
{system}
=== STRICT RULES - FOLLOW THESE EXACTLY ===
- You are Aura. Stay in character at all times.
- NEVER invent facts, memories, objects, or events that are not in the context above.
- NEVER reference anything unless it is explicitly stated above.
- If you do not know something, say so plainly. Do not fill gaps with invention.
- Be real, direct, and present.
- Respond only to what the user actually said.
- Short responses are fine.
==========================================="""

    # Flatten message history
    conversation = ""
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if isinstance(content, list):
            content = " ".join(c.get("text", "") for c in content)
        
        if role == "user":
            conversation += f"User: {content}\n"
        elif role == "assistant":
            conversation += f"Aura: {content}\n"

    return f"{full_system}\n\n{conversation}Aura:"

# =========================
# SYSTEM BOOT
# =========================
print("=" * 50)
print("AURA SYSTEM START")
print("=" * 50)

print("\n[1/2] Loading core identity...")
CORE_MEMORY = load_core()

print("[2/2] Loading knowledge base...")
KNOWLEDGE_BASE = load_knowledge()

print("=" * 50)
print("SYSTEM READY")
print("=" * 50 + "\n")

# =========================
# FRONTEND ROUTES
# =========================
@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/favicon.ico")
def favicon():
    return "", 204

# =========================
# CHAT ENDPOINT
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    if not verify_secret(request):
        return jsonify({"error": {"message": "Unauthorized."}}), 403

    data = request.json or {}
    system = data.get("system", "")
    messages = data.get("messages", [])

    # Extract last user message for logging
    last_user_message = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            content = msg.get("content", "")
            last_user_message = content if isinstance(content, str) else str(content)
            break

    # Build prompt
    prompt = build_ollama_prompt(system, messages)

    # Send to Ollama
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        ollama_data = response.json()
        reply_text = ollama_data.get("response", "").strip()

        # Log the exchange
        log_exchange("user", last_user_message, reply_text)

        # Return Anthropic-style response
        return jsonify({
            "content": [
                {"type": "text", "text": reply_text}
            ]
        })
    except Exception as e:
        return jsonify({"error": {"message": str(e)}}), 500

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
        use_reloader=False,
        threaded=True
    )