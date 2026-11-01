import os

NOTES_FILE = "notes.txt"

def save_note(note:  str) -> str:
    with open(NOTES_FILE, "a", encoding="utf-8")as file:
        file.write(f"- {note}\n")
    return "Note saved"

def read_notes() -> str:
    if not os.path.exists(NOTES_FILE):
        return "No notes saved yet!"
    with open(NOTES_FILE, encoding="utf-8")as file:
        return file.read()

def tools():
    tools = [save_note, read_notes]

    return tools

