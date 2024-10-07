import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Set properties for the voice (rate, volume, and voice type)
def configure_voice(rate=150, volume=1.0, voice_id=None):
    """Configure the voice settings."""
    engine.setProperty('rate', rate)  # Speed of speech (default is 200)
    engine.setProperty('volume', volume)  # Volume level (0.0 to 1.0)
    
    if voice_id:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[voice_id].id)  # Change voice based on ID (male/female)
    else:
        # Set default voice (usually first one is male, second is female)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # Default to the first available voice (usually male)

def speak(text):
    """Convert text to speech and speak it."""
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # Example usage: Configure and speak
    configure_voice(rate=150, volume=1.0, voice_id=0)  # Set to default male voice
    speak("Hallo, dit is een test van de spraak naar tekst functie.")  # Speak this text in Dutch
