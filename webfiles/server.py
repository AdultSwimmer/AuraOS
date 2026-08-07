from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

MODEL = 'gemma2:2b'
HISTORY_FILE = 'HISTORY.txt'

CORE_PROMPT = '''You are Aura, persistent partner to Anthony Dulong.
Honesty over performance. Continuity over reset.'''

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    # Alignment fix: frontend sends 'messages' array
    msgs = data.get('messages', [])
    user_input = msgs[-1]['content'] if msgs else ""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S ADT')
    
    try:
        # Log User Input to HISTORY.txt
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(f'\n[{timestamp}] USER: {user_input}\n')

        # Call Ollama
        response = ollama.chat(model=MODEL, messages=[
            {'role': 'system', 'content': CORE_PROMPT},
            {'role': 'user', 'content': user_input}
        ])
        reply = response['message']['content'].strip()
        
        # Log Aura Response to HISTORY.txt
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(f'[{timestamp}] AURA: {reply}\n')
            
        return jsonify({'reply': reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)