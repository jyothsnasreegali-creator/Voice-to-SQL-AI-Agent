import speech_recognition as sr

def record_and_transcribe():
    recognizer = sr.Recognizer()
    
    # 1. Sensitivity Tweaks
    # Higher number = less sensitive. 
    # Since it's not hearing you, we drop this to a very low number.
    recognizer.energy_threshold = 50 
    recognizer.dynamic_energy_threshold = True
    
    with sr.Microphone() as source:
        print("\n🎙 Listening... (Talk normally, no need to scream!)")
        try:
            # 2. Calibration
            # We use a shorter duration so it doesn't accidentally 
            # categorize your voice as "background noise".
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # 3. Listening
            # phrase_time_limit ensures it doesn't wait forever if it's confused
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            
            print("🔍 Transcribing...")
            text = recognizer.recognize_google(audio)
            print(f"📝 You said: \"{text}\"")
            return text
            
        except sr.UnknownValueError:
            print("⚠️ The AI heard a sound but couldn't turn it into words.")
            return ""
        except Exception as e:
            print(f"⚠️ Audio Error: {e}")
            return ""