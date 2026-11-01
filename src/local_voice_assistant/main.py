from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from local_voice_assistant.agent_tools_instructions.instructions import instruction
from local_voice_assistant.agent_tools_instructions.tools import tools
from local_voice_assistant.voice_assistant.speech_to_text import listen
from local_voice_assistant.voice_assistant.text_to_speech import speak

model = OpenAIChatModel(
    "qwen3.5:2b",
    provider=OllamaProvider(base_url="http://localhost:11434/v1"),
)

NOTES_FILE = "notes.txt"

agent = Agent(
    model,
    tools = tools(),
    instructions = instruction()
)

def start_assistant():
    print("Local agent ready! Type 'quit' to exit. \n")
    history = []
    while True:
        user_input = listen()
        if user_input.strip().lower() in ("quit","exit"):
            break
        result = agent.run_sync(user_input, message_history=history)
        history = result.all_messages()
        print(f"\n Agent: {result.output}\n")
        speak(result.output)

if __name__ == "__main__":
    start_assistant()