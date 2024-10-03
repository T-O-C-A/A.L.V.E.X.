from flask import Flask, request, jsonify
import openai
import os
import platform
import psutil

app = Flask(__name__)

# Set up OpenAI API Key
openai.api_key = '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'  # Replace this with your actual OpenAI API key

# Function to get GPT-4 response
def get_gpt_response(prompt):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# System control functions
def open_app(app_name):
    if platform.system() == "Windows":
        os.system(f'start {app_name}')
    elif platform.system() == "Darwin":  # macOS
        os.system(f'open -a "{app_name}"')
    elif platform.system() == "Linux":
        os.system(f'{app_name} &')

def control_system(command):
    if command == "shutdown":
        if platform.system() == "Windows":
            os.system('shutdown /s /f /t 0')
        elif platform.system() == "Linux":
            os.system('sudo shutdown now')
        elif platform.system() == "Darwin":
            os.system('sudo shutdown -h now')
    elif command == "restart":
        if platform.system() == "Windows":
            os.system('shutdown /r /t 0')
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            os.system('sudo reboot')

def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    return f"CPU Usage: {cpu_percent}%, Memory Usage: {memory_info.percent}%"

# Endpoint to process text/voice input
@app.route('/process', methods=['POST'])
def process_request():
    data = request.json
    input_text = data.get("input", "").lower()

    # Check if the command is system-related
    if "open" in input_text:
        app_name = input_text.split("open ")[1]
        open_app(app_name)
        return jsonify({"response": f"Opening {app_name}"})
    elif "shutdown" in input_text:
        control_system("shutdown")
        return jsonify({"response": "Shutting down the system."})
    elif "restart" in input_text:
        control_system("restart")
        return jsonify({"response": "Restarting the system."})
    elif "system info" in input_text:
        system_info = get_system_info()
        return jsonify({"response": system_info})

    # Otherwise, get response from GPT
    response = get_gpt_response(input_text)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
