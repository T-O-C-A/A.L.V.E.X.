# backend/feedback.py
import json

def submit_feedback(user, feedback_text):
    """
    Store the user's feedback in the feedback.json file.
    """
    feedback_path = "logs/feedback.json"
    try:
        with open(feedback_path, "r") as f:
            feedback_data = json.load(f)
    except FileNotFoundError:
        feedback_data = {}

    feedback_data.setdefault(user, []).append(feedback_text)

    with open(feedback_path, "w") as f:
        json.dump(feedback_data, f, indent=4)

    print(f"Feedback from {user} submitted successfully.")
