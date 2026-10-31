# 🎙️ Local Voice Assistant

Ask by voice, get a helpful reply, and hear it spoken aloud. The assistant can also tell the time, do simple calculations, and save notes.

### ✨ Features

- Voice input and spoken replies
- Local AI responses with Ollama
- Time, calculator, and notes tools

### 🚀 Quick start

Install the required packages:

```bash
pip install pydantic-ai openai SpeechRecognition sounddevice pyaudio
```

Start Ollama with the models used in the code (`qwen3.5:2b` and `phonon`), then run:

```bash
python agent.py
```

Say **“quit”** or **“exit”** to stop. Notes are saved to `notes.txt`.

### 📁 Files

`agent.py` · `speech_to_text.py` · `text_to_speech.py`

> **Privacy:** AI and speech output use local Ollama. Voice recognition uses Google's service and requires internet access.
