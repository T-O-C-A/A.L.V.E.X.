# backend/command_handler.py

def execute_command(user, command):
    """
    Execute a given command for a specific user.
    This is a placeholder for the actual command execution logic.
    """
    if command == "open_browser":
        # Logic to open the browser
        print(f"User {user} opened the browser.")
    elif command == "shutdown_computer":
        # Logic to shut down the computer
        print(f"User {user} shut down the computer.")
    else:
        print(f"User {user} executed command: {command}")

    # Add more command handling logic here
