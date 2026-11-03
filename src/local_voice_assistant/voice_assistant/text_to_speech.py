import threading
from collections import deque
from typing import Optional

import numpy as np
import sounddevice as sd
import speech_recognition as sr
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

MIC_RATE = 16000
BLOCK = 1600  # 100 ms per block


def speak(text: str) -> None:
    """Plain speech, no interruption."""
    speak_interruptible(text, allow_interrupt=False)


def speak_interruptible(
    text: str,
    allow_interrupt: bool = True,
    energy_threshold: float = 1500,   # minimum loudness to count as your voice
    trigger_blocks: int = 3,          # ~300 ms of loud sound = interruption
    silence_blocks: int = 12,         # ~1.2 s of silence = you finished talking
    grace_blocks: int = 10,           # first ~1 s: only measure the speaker echo
    preroll_blocks: int = 10,         # keep ~1 s before the trigger (no clipped words)
    max_record_blocks: int = 300,     # max ~30 s of recording
    retry_with_listen: bool = True,   # if not understood, ask again with listen()
    debug: bool = False,              # True = print loudness numbers (for tuning)
) -> Optional[str]:
    stop = threading.Event()

    def talk():
        try:
            with client.audio.speech.with_streaming_response.create(
                model="phonon",
                voice="default",
                input=text,
                response_format="pcm",
            ) as response:
                with sd.RawOutputStream(
                    samplerate=24000, channels=1, dtype="int16"
                ) as out:
                    for chunk in response.iter_bytes(chunk_size=4096):
                        if stop.is_set():
                            out.abort()
                            break
                        out.write(chunk)
        except Exception as e:
            print(f"❌ TTS error: {e}")

    player = threading.Thread(target=talk, daemon=True)
    player.start()

    if not allow_interrupt:
        player.join()
        return None

    print("🔊 Speaking... (talk anytime to interrupt)")

    preroll = deque(maxlen=preroll_blocks)   # audio just before the trigger
    frames = []                              # the actual recording
    loud, quiet, recording = 0, 0, False
    echo_levels, n, thr = [], 0, energy_threshold
    end_thr = energy_threshold * 0.4

    with sd.InputStream(
        samplerate=MIC_RATE, channels=1, dtype="int16", blocksize=BLOCK
    ) as mic:
        while True:
            block, _ = mic.read(BLOCK)
            rms = float(np.sqrt(np.mean(block.astype(np.float32) ** 2)))
            n += 1

            if not recording:
                if not player.is_alive():
                    return None  # agent finished, nobody interrupted

                if n <= grace_blocks:      # measure how loud the echo is
                    echo_levels.append(rms)
                    preroll.append(block)
                    continue

                # you must be clearly louder than the agent's own voice
                thr = max(energy_threshold, 2.0 * max(echo_levels))
                end_thr = max(thr * 0.4, 500)   # below this = silence
                if debug:
                    print(f"rms={rms:.0f}  thr={thr:.0f}")

                preroll.append(block)
                loud = loud + 1 if rms > thr else 0
                if loud >= trigger_blocks:
                    print("✋ Interrupted! Listening to you...")
                    stop.set()
                    recording = True
                    frames = list(preroll)   # include audio from before the trigger
            else:
                frames.append(block)
                quiet = quiet + 1 if rms < end_thr else 0
                if quiet >= silence_blocks or len(frames) > max_record_blocks:
                    break

    player.join()

    print("🔍 Recognizing...")
    raw = b"".join(f.tobytes() for f in frames)
    audio = sr.AudioData(raw, MIC_RATE, 2)
    try:
        heard = sr.Recognizer().recognize_google(audio)
        print(f"USER SPOKE: {heard}")
        return heard.lower()
    except sr.UnknownValueError:
        print("❌ Couldn't understand what you said.")
    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {e}")
        return None

    # Not understood -> ask again using the normal listen()
    if retry_with_listen:
        from local_voice_assistant.voice_assistant.speech_to_text import listen
        print("🎤 Please say that again...")
        return listen()

    return None


if __name__ == "__main__":
    speak_interruptible("Hello! This is a test. Try talking over me to interrupt.")