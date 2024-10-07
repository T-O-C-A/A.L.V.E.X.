import whisper
import os
import pyaudio
import wave

# Initialize Whisper model (load the base or small model for faster performance)
model = whisper.load_model("base")  # You can also use "small", "medium", or "large"

def record_audio(filename="command.wav"):
    """Records audio from the microphone and saves it to a file"""
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1  # Mono audio
    rate = 44100  # Record at 44.1kHz

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print("Recording...")

    stream = p.open(format=sample_format, channels=channels, rate=rate,
                    frames_per_buffer=chunk, input=True)

    frames = []  # Initialize array to store frames

    # Record for 5 seconds
    for _ in range(0, int(rate / chunk * 5)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Finished recording")

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(filename="command.wav"):
    """Transcribe the audio file to text using Whisper"""
    result = model.transcribe(filename)
    return result['text']

if __name__ == "__main__":
    # Test the recording and transcription
    record_audio()  # Record audio from the microphone
    command = transcribe_audio()  # Transcribe the recorded audio
    print(f"Transcribed Command: {command}")
