import os
import json
import requests

RAW_DIR = r"C:\Aura\knowledge\raw"
PROCESSED_DIR = r"C:\Aura\knowledge\processed"

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3"

os.makedirs(PROCESSED_DIR, exist_ok=True)


# =========================
# ASK OLLAMA
# =========================
def ask_ollama(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]


# =========================
# PROCESS FILE
# =========================
def process_file(path):

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    prompt = f"""
You are processing long-term conversational memory.

IMPORTANT:
- Preserve chronology.
- Preserve evolution of ideas.
- Preserve contradictions.
- Preserve uncertainty.
- Preserve emotional context.
- Preserve philosophical development.
- Preserve identity continuity.

Do NOT flatten the conversation into sterile summaries.

Return:
1. Main themes
2. Important concepts
3. Evolving ideas
4. Contradictions or revisions
5. Emotional tone shifts
6. Important continuity moments
7. Condensed contextual summary

Conversation:

{content}
"""

    result = ask_ollama(prompt)

    return {
        "source_file": os.path.basename(path),
        "processed_memory": result
    }


# =========================
# MAIN
# =========================
def main():

    files = [
        f for f in os.listdir(RAW_DIR)
        if f.endswith(".txt")
    ]

    for file in files:

        full_path = os.path.join(RAW_DIR, file)

        print(f"\nPROCESSING: {file}")

        processed = process_file(full_path)

        out_name = file.replace(".txt", ".json")

        out_path = os.path.join(PROCESSED_DIR, out_name)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(processed, f, indent=2)

        print(f"SAVED: {out_name}")


if __name__ == "__main__":
    main()