import os

from speech_to_text import listen
from text_to_speech import speak
from datetime import datetime

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

model = OpenAIChatModel(
    "qwen3.5:2b",
    provider=OllamaProvider(base_url="http://localhost:11434/v1"),
)

NOTES_FILE = "notes.txt"

def get_current_time() -> str:
    return datetime.now().strftime("%A, %B, %d, %Y at %I:%M  %p")

def calculation(expression: str) -> str:
    if not set(expression) <= set("0123456789+-*/(). "):
        return "Error : Only Number and + - * / () are allowed"
    try:
        return str(eval(expression))
    except Exception as error:
        return f"Error: {error}"

def save_note(note:  str) -> str:
    with open(NOTES_FILE, "a", encoding="utf-8")as file:
        file.write(f"- {note}\n")
    return "Note saved"

def read_notes() -> str:
    if not os.path.exists(NOTES_FILE):
        return "No notes saved yet!"
    with open(NOTES_FILE, encoding="utf-8")as file:
        return file.read()


agent = Agent(
    model,
    tools = [get_current_time, calculation, save_note, read_notes],
    instructions=(
        "You are a helpful personal assistant running 100% locally."
        "Use your tools whenever they can help answer the question."
        "Keep your answer short and friendly."
    )
)

def main():
    print("Local agent ready! Type 'quit' to exit. \n")
    history = []
    while True:
        print("You: ")
        #user_input = input("You: ")
        user_input = listen()
        if user_input.strip().lower() in ("quit","exit"):
            break
        result = agent.run_sync(user_input, message_history=history)
        history = result.all_messages()
        print(f"\n Agent: {result.output}\n")
        speak(result.output)

if __name__ == "__main__":
    main()