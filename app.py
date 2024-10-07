from flask import Flask, request, jsonify
from nlp_processing import process_nlp_input
from adaptive_learning import track_command_usage, analyze_feedback
from external_screen import ALVEXScreen
from task_scheduler import schedule_task
from ai_prediction import log_user_behavior, predict_next_action
from hand_tracking import start_hand_tracking_for_buttons
from user_profiles import update_user_profile
from workflow_templates import execute_workflow, add_custom_workflow
import threading

app = Flask(__name__)

# Start GUI projection
screen = ALVEXScreen()

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

# Start hand tracking in a separate thread
def start_hand_tracking():
    start_hand_tracking_for_buttons(screen)

if __name__ == '__main__':
    threading.Thread(target=start_hand_tracking).start()
    app.run(debug=True, port=5000)
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