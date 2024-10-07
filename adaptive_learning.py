import json
import os

# Define the file where command usage and feedback data will be stored
COMMAND_USAGE_FILE = "logs/command_usage.json"
FEEDBACK_FILE = "logs/feedback.json"

# Load existing command usage data
if os.path.exists(COMMAND_USAGE_FILE):
    with open(COMMAND_USAGE_FILE, 'r') as f:
        command_usage_data = json.load(f)
else:
    command_usage_data = {}

# Load existing feedback data
if os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, 'r') as f:
        feedback_data = json.load(f)
else:
    feedback_data = {}

# Function to track command usage
def track_command_usage(command):
    """Track the usage of each command."""
    if command not in command_usage_data:
        command_usage_data[command] = {"count": 0, "automated": False}
    command_usage_data[command]["count"] += 1

    # Save the updated command usage data
    with open(COMMAND_USAGE_FILE, 'w') as f:
        json.dump(command_usage_data, f, indent=4)

    # Check if automation should be suggested
    return suggest_automation(command)

# Function to suggest automation of frequently used commands
def suggest_automation(command):
    """Suggest automating a command if it is used frequently."""
    if command_usage_data[command]["count"] >= 5 and not command_usage_data[command]["automated"]:
        return f"The command '{command}' has been used {command_usage_data[command]['count']} times. Would you like to automate this command?"
    return None

# Function to automate a command
def automate_command(command):
    """Mark a command as automated."""
    if command in command_usage_data:
        command_usage_data[command]["automated"] = True
        with open(COMMAND_USAGE_FILE, 'w') as f:
            json.dump(command_usage_data, f, indent=4)
        return f"The command '{command}' has been automated."
    return f"Command '{command}' not found in the usage data."

# Function to analyze feedback and improve commands
def analyze_feedback(command, success, feedback_message=None):
    """Analyze user feedback for each command and suggest improvements."""
    if command not in feedback_data:
        feedback_data[command] = {"positive": 0, "negative": 0, "feedback": []}

    if success:
        feedback_data[command]["positive"] += 1
    else:
        feedback_data[command]["negative"] += 1

    if feedback_message:
        feedback_data[command]["feedback"].append(feedback_message)

    # Save feedback data
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback_data, f, indent=4)

    # Suggest improvements based on feedback
    return suggest_improvement(command)

# Function to suggest improvements based on feedback
def suggest_improvement(command):
    """Suggest improvements for commands with
