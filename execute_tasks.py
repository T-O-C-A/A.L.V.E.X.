import os

def execute_command(command):
    """Interpret and execute commands"""
    command = command.lower()  # Ensure command is in lowercase
    
    if "open browser" in command:
        os.system("start chrome")  # Replace with the relevant app command for your system
        print("Opening browser...")
    elif "shutdown" in command:
        os.system("shutdown /s /f /t 0")
        print("Shutting down the system...")
    elif "restart" in command:
        os.system("shutdown /r /t 0")
        print("Restarting the system...")
    elif "cpu usage" in command:
        # You can call your system monitoring module here
        print("Fetching CPU usage...")
    else:
        print(f"Unknown command: {command}")
