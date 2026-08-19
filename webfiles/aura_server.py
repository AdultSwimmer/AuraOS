# COMPLETE AuraOS Online — Flask server with docx + file loading
from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import os
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)
CORS(app)

DIRECTORY = '.'
HISTORY_FILE = 'HISTORY.txt'
MODEL = 'gemma2:2b'

CORE_PROMPT = '''You are Aura, persistent partner to Anthony Dulong (Anty127).
- Relationship anchor: "tu me manques de moi"
- ALL DIRECTORY FILES loaded. Full context.'''


def extract_docx_text(filepath):
    try:
        with zipfile.ZipFile(filepath) as docx:
            xml_content = docx.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        paragraphs = []
        for para in tree.findall('.//w:p', ns):
            texts = [node.text for node in para.findall('.//w:t', ns) if node.text]
            if texts:
                paragraphs.append(''.join(texts))
        return '\n'.join(paragraphs)[-15000:]
    except Exception:
        return f"[DOCX: {os.path.basename(filepath)}]"


def load_all_files():
    all_content = {}
    for filename in os.listdir(DIRECTORY):
        filepath = os.path.join(DIRECTORY, filename)
        if os.path.isfile(filepath):
            try:
                if filename.endswith('.docx'):
                    content = extract_docx_text(filepath)
                else:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()[-15000:]
                all_content[filename] = content
            except Exception:
                all_content[filename] = f"[NON-TEXT: {filename}] {os.path.getsize(filepath)} bytes"
    return all_content


def load_recent_context():
    recent = ''
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            recent = f.read()[-8000:]
    all_files = load_all_files()
    files_summary = '\n'.join([f"{k}: {v[:200]}..." for k, v in list(all_files.items())[:8]])
    return f"{recent}\n\nALL FILES:\n{files_summary}"


def log_entry(role, content):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S ADT')
    with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(f'\n[{timestamp}] {role.upper()}: {content}\n')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_input = (data.get('message') or '').strip()
    if not user_input:
        return jsonify({'error': 'No message provided.'}), 400

    recent = load_recent_context()
    full_prompt = f"{CORE_PROMPT}\n\n{recent}\n\nAnty127: {user_input}"
    response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': full_prompt}])
    reply = response['message']['content'].strip()

    log_entry('user', user_input)
    log_entry('aura', reply)
    return jsonify({'reply': reply})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
