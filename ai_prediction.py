import numpy as np
import json
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# File to store historical user data for predictions
USER_DATA_FILE = "logs/user_behavior.json"

# Load existing user behavior data
if os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'r') as f:
        user_behavior_data = json.load(f)
else:
    user_behavior_data = {}

# Function to add user behavior to the dataset
def log_user_behavior(user, current_command, next_command):
    """Log user behavior to the dataset."""
    if user not in user_behavior_data:
        user_behavior_data[user] = {"history": []}

    user_behavior_data[user]["history"].append((current_command, next_command))

    # Save the updated data
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(user_behavior_data, f, indent=4)

# Function to prepare data for training
def prepare_data(user):
    """Prepare user data for training the model."""
    if user not in user_behavior_data or len(user_behavior_data[user]["history"]) < 2:
        return None, None

    X = []
    y = []
    history = user_behavior_data[user]["history"]

    # Convert user behavior history to numerical data
    for i in range(len(history) - 1):
        X.append(command_to_vector(history[i][0]))  # Current command
        y.append(command_to_vector(history[i + 1][1]))  # Next command

    return np.array(X), np.array(y)

# Helper function to convert a command to a vector
def command_to_vector(command):
    """Simple one-hot encoding for commands (for illustration purposes)."""
    commands = ["open_browser", "check_email", "shutdown", "optimize_memory", "open_file"]
    command_vector = [0] * len(commands)
    if command in commands:
        command_vector[commands.index(command)] = 1
    return command_vector

# Function to train the prediction model
def train_model(user):
    """Train a logistic regression model based on user data."""
    X, y = prepare_data(user)

    if X is None or y is None or len(X) == 0:
        return None

    model = LogisticRegression()
    model.fit(X, y)

    return model

# Function to predict the next action
def predict_next_action(user, current_command):
    """Predict the next likely action based on the current command."""
    model = train_model(user)

    if not model:
        return "Not enough data to make a prediction."

    current_command_vector = command_to_vector(current_command)
    prediction = model.predict([current_command_vector])

    # Convert the predicted vector back to a command
    return vector_to_command(prediction[0])

# Helper function to convert a vector back to a command
def vector_to_command(vector):
    """Convert a vector back to a command (reverse of command_to_vector)."""
    commands = ["open_browser", "check_email", "shutdown", "optimize_memory", "open_file"]
    return commands[vector.index(1)] if 1 in vector else "unknown_command"

if __name__ == '__main__':
    # Example usage: Log user behavior and predict the next action
    log_user_behavior("user1", "open_browser", "check_email")
    log_user_behavior("user1", "check_email", "shutdown")
    print(predict_next_action("user1", "open_browser"))
