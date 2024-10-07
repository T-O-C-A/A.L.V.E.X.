from flask import Flask, request, jsonify
from nlp_processing import process_nlp_input
from adaptive_learning import automate_command, track_command_usage, analyze_feedback
from external_screen import ALVEXScreen
from task_scheduler import execute_predefined_command, remove_task, schedule_task
from ai_prediction import log_user_behavior, predict_next_action
from hand_tracking import start_hand_tracking_for_buttons
from user_profiles import update_user_profile, get_user_profile, add_frequent_command, suggest_frequent_commands, clear_user_profile
from workflow_templates import execute_workflow, add_custom_workflow
from cross_platform import control_smart_device, sync_task, get_synced_task, get_device_status
from security import encrypt_data, decrypt_data, authenticate_user, log_command, save_encrypted_file, load_decrypted_file
from system_monitor import monitor_cpu_usage, monitor_memory_usage, monitor_disk_usage, suggest_system_optimizations
import threading

app = Flask(__name__)

# Start GUI projection
screen = ALVEXScreen()

# Start hand tracking in a separate thread
def start_hand_tracking():
    start_hand_tracking_for_buttons(screen)

if __name__ == '__main__':
    threading.Thread(target=start_hand_tracking).start()
    app.run(debug=True, port=5000)

@app.route('/execute_command', methods=['POST'])
def execute_command():
    command = request.json.get('command', '').lower()
    user = request.json.get('user', 'default')

    # Display the command on the external screen
    screen.update_text(f"Executing: {command}")

    # Log the current and next command after each execution (for prediction)
    previous_command = "your_previous_command"  # This would be stored from previous execution
    log_user_behavior(user, previous_command, command)

    # Execute the command (actual command execution logic here)
    result = execute_predefined_command(command) 

    # Predict the next likely action
    next_action_prediction = predict_next_action(user, command)

    return jsonify({"response": result, "next_action_prediction": next_action_prediction})

@app.route('/provide_feedback', methods=['POST'])
def provide_feedback():
    command = request.json.get('command', '')
    success = request.json.get('success', True)
    feedback_message = request.json.get('feedback_message', None)

    # Analyze feedback and suggest improvements if needed
    improvement_suggestion = analyze_feedback(command, success, feedback_message)
    return jsonify({"response": f"Feedback for '{command}' recorded.", "suggestion": improvement_suggestion})

@app.route('/automate_command', methods=['POST'])
def automate_command_route():
    command = request.json.get('command', '')
    response = automate_command(command)
    return jsonify({"response": response})

@app.route('/ask_question', methods=['POST'])
def ask_question():
    question = request.json.get('question', '')
    options = request.json.get('options', [])

    # Display question on external screen and show options
    screen.update_text(question)
    screen.clear_buttons()

    for option in options:
        screen.add_button(option, lambda opt=option: screen.update_text(f"{opt} selected"), option)

    return jsonify({"response": f"Question '{question}' displayed with options {options}."})

@app.route('/execute_nlp_command', methods=['POST'])
def execute_nlp_command():
    command = request.json.get('command', '')
    translated_command = process_nlp_input(command)
    screen.update_text(f"Executing NLP command: {translated_command}")
    result = execute_predefined_command(translated_command)
    return jsonify({"response": result})

@app.route('/schedule_task', methods=['POST'])
def schedule_task_route():
    command = request.json.get('command')
    time_string = request.json.get('time_string')
    schedule_task(command, time_string)
    return jsonify({"response": f"Scheduled {command} at {time_string}"})

@app.route('/remove_task', methods=['POST'])
def remove_task_route():
    command = request.json.get('command')
    remove_task(command)
    return jsonify({"response": f"Task '{command}' has been removed."})

@app.route('/predict_next', methods=['POST'])
def predict_next():
    user_data = request.json.get('user_data')
    next_action = predict_next_action(user_data)
    return jsonify({"next_action": next_action})

@app.route('/execute_workflow', methods=['POST'])
def execute_workflow_route():
    workflow_name = request.json.get('workflow_name')
    result = execute_workflow(workflow_name)
    return jsonify({"response": result})

@app.route('/add_custom_workflow', methods=['POST'])
def add_custom_workflow_route():
    workflow_name = request.json.get('workflow_name')
    workflow_data = request.json.get('workflow_data')
    result = add_custom_workflow(workflow_name, workflow_data)
    return jsonify({"response": result})
@app.route('/control_device', methods=['POST'])
def control_device_route():
    device_name = request.json.get('device_name')
    action = request.json.get('action')
    device_api_url = request.json.get('device_api_url')
    api_key = request.json.get('api_key', None)

    response = control_smart_device(device_name, action, device_api_url, api_key)
    return jsonify({"response": response})

@app.route('/sync_task', methods=['POST'])
def sync_task_route():
    task_name = request.json.get('task_name')
    task_data = request.json.get('task_data')
    response = sync_task(task_name, task_data)
    return jsonify({"response": response})

@app.route('/get_synced_task', methods=['GET'])
def get_synced_task_route():
    task_name = request.args.get('task_name')
    response = get_synced_task(task_name)
    return jsonify({"response": response})

@app.route('/get_device_status', methods=['POST'])
def get_device_status_route():
    device_name = request.json.get('device_name')
    status_api_url = request.json.get('status_api_url')
    api_key = request.json.get('api_key', None)

    response = get_device_status(device_name, status_api_url, api_key)
    return jsonify({"response": response})

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    data = request.json.get('data')
    password = request.json.get('password')
    encrypted = encrypt_data(data, password)
    return jsonify({"encrypted_data": encrypted})

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    encrypted_data = request.json.get('encrypted_data')
    password = request.json.get('password')
    decrypted = decrypt_data(encrypted_data, password)
    return jsonify({"decrypted_data": decrypted})

@app.route('/authenticate', methods=['POST'])
def authenticate_route():
    username = request.json.get('username')
    password = request.json.get('password')
    use_mfa = request.json.get('use_mfa', False)
    if authenticate_user(username, password, use_mfa):
        return jsonify({"response": "Authenticated successfully"})
    else:
        return jsonify({"response": "Authentication failed"}), 401

@app.route('/log_command', methods=['POST'])
def log_command_route():
    command = request.json.get('command')
    user = request.json.get('user')
    log_command(command, user)
    return jsonify({"response": f"Command '{command}' logged for user '{user}'."})

@app.route('/update_profile', methods=['POST'])
def update_profile_route():
    user = request.json.get('user')
    preference_key = request.json.get('preference_key')
    preference_value = request.json.get('preference_value')
    response = update_user_profile(user, preference_key, preference_value)
    return jsonify({"response": response})

@app.route('/get_profile', methods=['GET'])
def get_profile_route():
    user = request.args.get('user')
    response = get_user_profile(user)
    return jsonify({"response": response})

@app.route('/add_frequent_command', methods=['POST'])
def add_frequent_command_route():
    user = request.json.get('user')
    command = request.json.get('command')
    response = add_frequent_command(user, command)
    return jsonify({"response": response})

@app.route('/suggest_commands', methods=['GET'])
def suggest_commands_route():
    user = request.args.get('user')
    response = suggest_frequent_commands(user)
    return jsonify({"response": response})

@app.route('/clear_profile', methods=['POST'])
def clear_profile_route():
    user = request.json.get('user')
    response = clear_user_profile(user)
    return jsonify({"response": response})

@app.route('/monitor_cpu', methods=['GET'])
def monitor_cpu_route():
    cpu_usage = monitor_cpu_usage()
    return jsonify({"cpu_usage": cpu_usage})

@app.route('/monitor_memory', methods=['GET'])
def monitor_memory_route():
    memory_usage = monitor_memory_usage()
    return jsonify({"memory_usage": memory_usage})

@app.route('/monitor_disk', methods=['GET'])
def monitor_disk_route():
    disk = request.args.get('disk', '/')  # Default to root partition
    disk_usage = monitor_disk_usage(disk)
    return jsonify({"disk_usage": disk_usage})

@app.route('/suggest_optimizations', methods=['GET'])
def suggest_optimizations_route():
    suggestions = suggest_system_optimizations()
    if isinstance(suggestions, list):
        return jsonify({"suggestions": suggestions})
    else:
        return jsonify({"message": suggestions})