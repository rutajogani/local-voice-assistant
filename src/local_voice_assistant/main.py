from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from local_voice_assistant.agent_tools_instructions.instructions import instruction
from local_voice_assistant.agent_tools_instructions.tools import tools
from local_voice_assistant.voice_assistant.speech_to_text import listen
from local_voice_assistant.voice_assistant.text_to_speech import speak_interruptible

model = OpenAIChatModel(
    "qwen3.5:2b",
    provider=OllamaProvider(base_url="http://localhost:11434/v1"),
)

NOTES_FILE = "notes.txt"

agent = Agent(
    model,
    tools=tools(),
    instructions=instruction(),
)


def start_assistant():
    print("Local agent ready! Say 'quit' or 'exit' to stop.\n")
    history = []
    user_input = None  # nothing to answer yet

    while True:
        # Only open the mic if we don't already have an interrupt phrase
        if not user_input:
            user_input = listen()
            if not user_input:      # listen() returned None (nothing understood)
                continue

        if user_input.strip().lower() in ("quit", "exit"):
            break

        result = agent.run_sync(user_input, message_history=history)
        history = result.all_messages()
        print(f"\n Agent: {result.output}\n")

        # Speak the answer. If you talk over it, speech stops and your words
        # come back here as the next input. If nobody interrupts, this returns
        # None and the loop calls listen() again.
        user_input = speak_interruptible(result.output)


if __name__ == "__main__":
    start_assistant()