import os

from local_voice_assistant.agent_tools_instructions.query_db import (
    run_command,
    run_query,
)

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

def select_query(sql: str, params: tuple | None = None) -> list[dict]:
    return run_query(sql, params)

def query_command(sql: str, params: tuple | None = None) -> int:
    return run_command(sql, params)

def tools():
    tools = [save_note, read_notes, select_query, query_command]

    return tools

