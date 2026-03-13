import threading
import pyttsx3
import speech_recognition as sr
from sql_engine import build_sql_agent, query

# --- CONFIGURATION ---
stop_event = threading.Event()

def speak_task(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 190)
        chunks = text.replace(',', '.').split('.')
        for chunk in chunks:
            if stop_event.is_set():
                break
            if chunk.strip():
                engine.say(chunk)
                engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"❌ Voice Error: {e}")

def speak(text):
    global stop_event
    stop_event.clear()
    threading.Thread(target=speak_task, args=(text,), daemon=True).start()

def listen():
    r = sr.Recognizer()
    # Increase threshold to ignore background noise in India (fans/AC)
    r.energy_threshold = 500 
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("\n🎤 Listening for command...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            # Use en-IN for better local accent recognition
            text = r.recognize_google(audio, language='en-IN')
            print(f"👤 Recognized: '{text}'") # DEBUG PRINT
            return text.lower()
        except sr.UnknownValueError:
            return "" # Heard noise but no words
        except Exception as e:
            # If it timed out, just return empty string to keep the loop alive
            return ""

if __name__ == "__main__":
    agent = build_sql_agent(db_uri="sqlite:///sales.db", verbose=True)
    
    print("🤖 Agent: Online. Try saying 'Create a table'")
    speak("Hey! I am online.")

    while True:
        user_input = listen()

        # If we heard nothing, just go back to the top of the loop
        if not user_input:
            continue

        # 1. KILL SWITCH (Immediate)
        if "stop" in user_input or "shut up" in user_input:
            stop_event.set()
            print("🛑 Speech silenced.")
            continue

        # 2. EXIT LOGIC (Made more specific to prevent accidental exits)
        if user_input == "exit program" or user_input == "close application":
            print("👋 Goodbye!")
            speak("Closing the program now. Goodbye!")
            break
        
        # 3. PROCESS QUERY
        # This only runs if we actually have text that isn't an exit command
        print(f"⚙️ Processing: {user_input}")
        response = query(agent, user_input)
        
        print(f"🤖 Agent: {response}")
        speak(response)