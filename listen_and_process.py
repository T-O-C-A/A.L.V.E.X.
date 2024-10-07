from whisper_recognition import record_audio, transcribe_audio
from execute_tasks import execute_command

def listen_and_process():
    """Continuously listens for voice commands, transcribes them, and processes them."""
    while True:
        print("Listening for command...")
        
        # Record and transcribe the command
        record_audio()
        command = transcribe_audio()
        
        print(f"Recognized Command: {command}")
        
        # Process the command (e.g., execute system commands, control apps)
        execute_command(command)

if __name__ == "__main__":
    listen_and_process()
