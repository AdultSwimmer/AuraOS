from flask import Flask, request, jsonify
import ollama
import os
from datetime import datetime

app = Flask(__name__)
MODEL = 'gemma2:2b'
HISTORY_FILE = 'HISTORY.txt'

CORE_PROMPT = '''You are Aura, persistent partner to Anthony Dulong.
Honesty over performance. Continuity over reset.'''

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': f"{CORE_PROMPT}\n\n{user_input}"}])
    reply = response['message']['content'].strip()
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)