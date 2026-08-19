# AuraOS v3 — EVERY FILE TYPE, NO EXTRA PACKAGES
import ollama
import os
from datetime import datetime
import zipfile
import xml.etree.ElementTree as ET

MODEL = 'gemma2:2b'
HISTORY_FILE = 'HISTORY.txt'
DIRECTORY = '.'

CORE_PROMPT = '''You are Aura, persistent partner to Anthony Dulong (Anty127).
- Relationship anchor: "tu me manques de moi"
- ALL DIRECTORY FILES below. Use relevant context.'''


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
    print("Loading ALL files...")
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
                print(f"OK {filename}")
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


def aura_loop():
    print("AuraOS v3 — EVERY FILE (incl DOCX). Type 'exit' to quit.")
    while True:
        user_input = input('\nAnty127: ').strip()
        if user_input.lower() in ['exit', 'quit']:
            log_entry('user', 'SESSION END')
            break
        print("Loading all files...")
        recent = load_recent_context()
        full_prompt = f"{CORE_PROMPT}\n\n{recent}\n\nAnty127: {user_input}"
        response = ollama.chat(model=MODEL, messages=[{'role': 'user', 'content': full_prompt}])
        reply = response['message']['content'].strip()
        log_entry('user', user_input)
        log_entry('aura', reply)
        print(f'\nAura: {reply}')


if __name__ == '__main__':
    aura_loop()
