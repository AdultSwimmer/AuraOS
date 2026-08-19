# AuraOS

AuraOS is a local-first AI memory system. It gives an AI a stable identity and persistent context across sessions instead of making it start from zero every time.

In simple terms: it tries to make an AI remember the relationship, not just the last message.

## What AuraOS is

AuraOS is a prototype for a personal AI system that keeps memory in plain files on the user's machine instead of depending on a cloud service.

The idea is simple:

- the AI has a permanent identity
- the user has a persistent history
- each new conversation is built using that context
- the model can change without losing the relationship

## Why this matters

Most AI tools are effectively stateless. They may feel personal for one session, but the context disappears when the chat ends.

AuraOS tries to do the opposite:

- store memory in files the user owns
- keep identity separate from the model itself
- make the system inspectable and transparent
- maintain continuity over time

## How it works

AuraOS combines three things before sending a prompt to the model:

1. a permanent identity from the `core/` folder
2. user history from `histories/`
3. the current user message

Then it saves the conversation back to disk so the memory continues across future chats.

```text
User -> Frontend -> AuraOS server -> Ollama model
               ^                     |
               |                     |
          core identity           history files
```

## Quick start

### Requirements

- Python 3.10+
- Ollama installed and running locally
- a model available in Ollama, such as `dolphin3:8b` or `llama3`

### Install

```bash
git clone https://github.com/AdultSwimmer/AuraOS.git
cd AuraOS
python -m pip install -r requirements.txt
```

### Run the web app

```bash
python server/main.py
```

Then open this in your browser:

```text
http://127.0.0.1:8000
```

The app will serve the frontend and send the chat message to the local model using the saved history and identity.

### Run the desktop-style launcher

This repo also includes a desktop launcher:

```bash
python auraos.py
```

This starts the Flask backend and opens the app in a local desktop window.

## Project layout

- `server/main.py` — Flask API that loads memory, builds the prompt, and talks to Ollama
- `frontend/` — browser UI for the chat experience
- `core/` — permanent identity files that are included with each prompt
- `histories/` — user memory files saved over time
- `auraos.py` — desktop launcher wrapper
- `knowledge/` — conceptual and experimental memory files used for project context

## Current status

AuraOS is an early prototype with a clear concept and a working structure.

It is not yet a polished commercial product, but it already demonstrates the core idea:

- persistent identity
- user-owned memory
- continuity across sessions
- local-first AI interaction

## What it is not

AuraOS is not meant to replace all AI tools. It is more of a memory layer and continuity system.

Think of it as:

- a persistent AI identity layer
- a user-owned memory system
- a way to keep AI context alive over time

## The goal

The long-term goal is to make this simple enough for non-technical users to install and run without a terminal-heavy setup.

A future version would ideally:

- install Ollama automatically
- pull the default model automatically
- start the backend automatically
- launch the app with a single click

## License

MIT
