import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")

            # Adjust for ambient noise 
            recognizer.adjust_for_ambient_noise(source, duration=1)

            # Wait until user speaks
            audio = recognizer.listen(source)

        print("🔍 Recognizing...")

        text = recognizer.recognize_google(audio)

        print(f"USER SPOKE: {text}")

        return text.lower()

    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return None

    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {e}")
        return None

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


if __name__ == "__main__":
    listen()
