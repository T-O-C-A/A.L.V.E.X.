import requests
import json
import os

# File to store shared tasks for cross-platform syncing
SYNC_FILE = "logs/cross_platform_sync.json"

# Load existing tasks for syncing
if os.path.exists(SYNC_FILE):
    with open(SYNC_FILE, 'r') as f:
        synced_tasks = json.load(f)
else:
    synced_tasks = {}

# Function to control smart devices via API
def control_smart_device(device_name, action, device_api_url, api_key=None):
    """
    Send a request to control a smart device via its API.
    
    :param device_name: The name of the smart device (e.g., "smart_light").
    :param action: The action to perform (e.g., "turn_on", "turn_off").
    :param device_api_url: The API endpoint to control the device.
    :param api_key: Optional API key for authorization.
    :return: Response message from the API.
    """
    headers = {}
    if api_key:
        headers['Authorization'] = f"Bearer {api_key}"
    
    data = {
        "device": device_name,
        "action": action
    }
    
    try:
        response = requests.post(device_api_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("message", f"{device_name} action '{action}' executed successfully.")
    except requests.exceptions.RequestException as e:
        return f"Failed to control {device_name}: {str(e)}"

# Function to sync tasks across platforms
def sync_task(task_name, task_data):
    """
    Sync a task across multiple platforms by saving it to a shared sync file.
    
    :param task_name: The name of the task to sync.
    :param task_data: The details of the task (e.g., parameters or steps).
    :return: Confirmation message.
    """
    synced_tasks[task_name] = task_data

    # Save the synced tasks to the file
    with open(SYNC_FILE, 'w') as f:
        json.dump(synced_tasks, f, indent=4)

    return f"Task '{task_name}' has been synced across platforms."

# Function to get a synced task
def get_synced_task(task_name):
    """
    Retrieve a synced task by its name.
    
    :param task_name: The name of the synced task to retrieve.
    :return: The details of the task, or a message if the task is not found.
    """
    if task_name in synced_tasks:
        return synced_tasks[task_name]
    else:
        return f"Task '{task_name}' not found."

# Function to monitor the status of smart devices
def get_device_status(device_name, status_api_url, api_key=None):
    """
    Check the status of a smart device via its API.
    
    :param device_name: The name of the smart device (e.g., "smart_light").
    :param status_api_url: The API endpoint to retrieve the device's status.
    :param api_key: Optional API key for authorization.
    :return: The status of the device.
    """
    headers = {}
    if api_key:
        headers['Authorization'] = f"Bearer {api_key}"

    try:
        response = requests.get(status_api_url, headers=headers)
        response.raise_for_status()
        return response.json().get("status", f"Unable to retrieve status for {device_name}.")
    except requests.exceptions.RequestException as e:
        return f"Failed to get status of {device_name}: {str(e)}"

# Example device control (you can modify this with actual device details)
def control_example_smart_light(action):
    """
    Example of controlling a smart light via a hypothetical API.
    
    :param action: Action to perform on the light (e.g., "turn_on" or "turn_off").
    """
    device_name = "smart_light"
    api_url = "https://api.example.com/devices/smart_light/actions"
    api_key = "your_api_key_here"  # Replace with your actual API key

    response = control_smart_device(device_name, action, api_url, api_key)
    print(response)

# Example usage: Control a smart light and sync tasks
if __name__ == "__main__":
    # Control a smart device (e.g., turn on the light)
    control_example_smart_light("turn_on")

    # Sync a task across platforms
    task_data = {"description": "Backup files", "time": "22:00"}
    print(sync_task("backup_files", task_data))

    # Get a synced task
    print(get_synced_task("backup_files"))

    # Monitor the status of a device (e.g., check if the smart light is on or off)
    device_status = get_device_status("smart_light", "https://api.example.com/devices/smart_light/status", "your_api_key_here")
    print(device_status)
