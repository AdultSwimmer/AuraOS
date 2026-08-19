# AuraOS

**Persistent memory harness for large language models.**

AuraOS is a lightweight wrapper that sits between a user and any LLM (local or remote). It gives the model a stable identity and long-term memory that survives across sessions, token limits, and model switches.

The model itself remains replaceable. The memory and identity stay with the user.

## What it does

- Loads a fixed **core identity** on every request
- Maintains a user-owned **HISTORY** file that persists indefinitely
- Injects relevant context automatically so the model never starts from zero
- Works with local models (Ollama, etc.) or remote APIs
- Keeps the human in control of the memory — nothing is stored on a vendor server

## Why it exists

Most LLM interactions are stateless. When the context window fills or the session ends, the relationship resets. AuraOS treats memory as a first-class, user-owned artifact instead of something the model (or the provider) controls.

## Quick start

### Requirements
- Python 3.10+
- Ollama (recommended for local use) or any OpenAI-compatible API

### Run locally

```bash
git clone https://github.com/yourusername/AuraOS.git
cd AuraOS
pip install -r requirements.txt

# Start the server
python server/main.py
```

Open `http://127.0.0.1:8000` in your browser.

### Core identity

Place any number of `.txt` or `.md` files in the `core/` directory.  
They are loaded in order and prepended to every conversation as the permanent system identity.

### Memory

Each user has a `HISTORY` file.  
This file is the single source of truth for long-term context.  
It can be exported, backed up, versioned, or moved between machines.

## Architecture

```
User ↔ Frontend ↔ AuraOS Server ↔ Model (Ollama / API)
                      ↑
                 core/ + HISTORY
```

The server is deliberately thin. It does three things:

1. Load core identity
2. Load and inject user history
3. Forward the assembled prompt to the model

Everything else is left to the model and the user.

## Design principles

- **User-owned memory** — History lives in plain files the user controls
- **Model-agnostic** — Swap the backend without losing identity or context
- **Minimal** — No account system required, no telemetry, no forced cloud
- **Transparent** — The full prompt that reaches the model can be inspected

## Status

Early public harness.  
The core loop works. Expect rough edges.

## License

MIT
