from flask import Flask, request, jsonify
import os
import psutil
import whisper
from execute_tasks import execute_command
from whisper_recognition import record_audio, transcribe_audio

app = Flask(__name__)

# Initialize Whisper model
whisper_model = whisper.load_model("base")  # You can change the model to small/medium/large if needed

# Endpoint for manual text command input (as backup for voice recognition)
@app.route('/process', methods=['POST'])
def process_command():
    data = request.json
    input_text = data.get("input", "").lower()
    print(f"Received text command: {input_text}")
    
    # Execute the command received via text input
    response = execute_command(input_text)
    
    return jsonify({"response": response})

# Endpoint to handle voice input and process commands via Whisper
@app.route('/process_voice', methods=['POST'])
def process_voice_command():
    # Step 1: Record and save audio from the microphone
    record_audio()  # This saves the command to a .wav file
    
    # Step 2: Transcribe the audio to text using Whisper
    transcribed_text = transcribe_audio()
    print(f"Recognized Command: {transcribed_text}")
    
    # Step 3: Execute the transcribed command
    response = execute_command(transcribed_text)
    
    return jsonify({"response": response})

# Endpoint to get system information (CPU, Memory, etc.)
@app.route('/system_info', methods=['GET'])
def system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    system_info_data = {
        "CPU Usage": f"{cpu_percent}%",
        "Memory Usage": f"{memory_info.percent}%"
    }
    return jsonify(system_info_data)

# Main route to listen and process commands via Whisper
@app.route('/listen', methods=['GET'])
def listen_and_process():
    """Listen continuously for voice commands and process them."""
    while True:
        print("Listening for a command...")
        
        # Record and transcribe the command using Whisper
        record_audio()
        transcribed_command = transcribe_audio()
        print(f"Transcribed Command: {transcribed_command}")
        
        # Execute the command
        response = execute_command(transcribed_command)
        print(f"Executed: {response}")
        
        # Return the response to the user
        return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
