# 🎙️ Local Voice Assistant

> A voice controlled personal assistant powered by Ollama, with spoken replies, note saving, and PostgreSQL tools.

Speak into your microphone, get an answer from a local language model, and hear the response aloud. The project can also save and read notes and look up or update data in a PostgreSQL database.

## ✨ What it can do

- **Listen and respond:** captures speech from your microphone and speaks the assistant’s reply.
- **Run a local language model:** sends chat requests to Ollama at `http://localhost:11434/v1` using `qwen3.5:2b`.
- **Speak with local text to speech:** uses Ollama’s OpenAI-compatible audio endpoint with the `phonon` model.
- **Save notes:** appends notes to `notes.txt` in the directory where you start the app.
- **Work with PostgreSQL:** lists tables, reads table schemas, runs read-only queries, and executes data changes when requested.

### ✨ Features

🎤 Voice input &nbsp; · &nbsp; 🧠 Local AI &nbsp; · &nbsp; 🔊 Spoken replies  
📝 Save notes &nbsp; · &nbsp; 🐘 PostgreSQL tools

# 🧰 Project structure

```text
ai-agent/
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── .python-version
└── src/
    └── local_voice_assistant/
        ├── __init__.py
        ├── main.py
        ├── agent_tools_instructions/
        │   ├── instructions.py
        │   ├── query_db.py
        │   └── tools.py
        └── voice_assistant/
            ├── speech_to_text.py
            └── text_to_speech.py
```

## ✅ Prerequisites

- Python version specified in `.python-version`
- [uv](https://docs.astral.sh/uv/) for installing the project dependencies
- [Ollama](https://ollama.com/) running locally, with `qwen3.5:2b` and `phonon` available
- A working microphone and audio output
- Docker, if you want to run PostgreSQL using the included Dockerfile

## 🚀 Get started

### 1. Install the Python dependencies

From the project root, sync the dependencies declared by the project:

```bash
uv sync
```

### 2. Start Ollama

Make sure Ollama is running and that the model names below match the models available to your Ollama installation:

```text
Chat model:  qwen3.5:2b
Speech model: phonon
```

The application connects to Ollama at `http://localhost:11434/v1`.

### 3. Start PostgreSQL

The included `Dockerfile` builds a PostgreSQL 16 container. From the project root:

```bash
docker build -t local-voice-assistant-db .
docker run --name local-voice-assistant-db -p 5432:5432 -d local-voice-assistant-db
```

The database configuration in `query_db.py` expects:

| Setting | Value |
| --- | --- |
| Host | `localhost` |
| Port | `5432` |
| Database | `appdb` |
| User | `postgres` |
| Password | `postgres` |

These are development defaults. If you change them, update `DB_CONFIG` in `query_db.py` to match. The Dockerfile does not create application tables; add any tables your assistant should use.

### 4. Run the assistant

```bash
uv run python -m local_voice_assistant.main
```

Speak after the “Listening...” prompt. Say **“quit”** or **“exit”** to leave the assistant.

## 🔐 Privacy and connectivity

Chat and speech generation are configured to use the local Ollama service. Speech recognition calls `recognize_google`, so microphone audio is sent to Google for transcription and an internet connection is required. PostgreSQL connection values are currently written directly in `query_db.py`; change them before using credentials beyond a local development setup.

## 📝 Notes

Notes are stored in `notes.txt` relative to the current working directory. Keep the assistant running from a directory where you want that file to be created.