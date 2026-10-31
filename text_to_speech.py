from openai import OpenAI
import sounddevice as sd

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

def speak(text):                      # now receives the text
    with client.audio.speech.with_streaming_response.create(
        model="phonon",
        voice="default",
        input=text,                   # use the text here
        response_format="pcm",
    ) as response:
        with sd.RawOutputStream(
            samplerate=24000,
            channels=1,
            dtype="int16",
        ) as audio:
            for chunk in response.iter_bytes(chunk_size=4096):
                audio.write(chunk)

if __name__ == "__main__":
    speak("")