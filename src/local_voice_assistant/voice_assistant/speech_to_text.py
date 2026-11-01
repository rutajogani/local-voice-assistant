from typing import Optional

import speech_recognition as sr


def listen(
    pause_threshold: float = 2.0,
    timeout: Optional[float] = 8,
    phrase_time_limit: Optional[float] = 30,
    max_attempts: int = 3,
) -> Optional[str]:
    """Listen to the microphone and return the recognized text (lowercase).

    Args:
        pause_threshold: Seconds of silence that count as "the user is done".
            Higher values let you pause mid-sentence without being cut off.
        timeout: Max seconds to wait for speech to START. None waits forever.
        phrase_time_limit: Max seconds for a single phrase. None means no limit.
        max_attempts: How many times to retry if nothing was understood.
    """
    recognizer = sr.Recognizer()

    # Silence needed before the phrase is considered finished (default 0.8)
    recognizer.pause_threshold = pause_threshold
    # Silence kept at the start/end of the audio so words aren't clipped (default 0.5)
    recognizer.non_speaking_duration = 0.5
    # Let the energy threshold adapt to room noise while listening
    recognizer.dynamic_energy_threshold = True
    recognizer.dynamic_energy_adjustment_damping = 0.15
    recognizer.dynamic_energy_ratio = 1.5

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)

            for attempt in range(1, max_attempts + 1):
                try:
                    print("🎤 Listening...")
                    audio = recognizer.listen(
                        source,
                        timeout=timeout,
                        phrase_time_limit=phrase_time_limit,
                    )
                except sr.WaitTimeoutError:
                    print("⏱️ No speech detected.")
                    continue

                print("🔍 Recognizing...")
                try:
                    text = recognizer.recognize_google(audio)
                except sr.UnknownValueError:
                    print(f"❌ Couldn't understand audio (attempt {attempt}/{max_attempts}).")
                    continue

                print(f"USER SPOKE: {text}")
                return text.lower()

    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {e}")
    except OSError as e:
        print(f"❌ Microphone error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    return None


if __name__ == "__main__":
    print(listen())