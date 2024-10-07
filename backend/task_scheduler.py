import schedule
import time
import psutil
import threading

# Define a dictionary to hold all scheduled tasks for management
scheduled_tasks = {}

# Function to schedule a task at a specific time
def schedule_task(command, time_string):
    """Schedule a task to run at a specific time."""
    job = schedule.every().day.at(time_string).do(execute_predefined_command, command)
    scheduled_tasks[command] = job
    print(f"Task '{command}' scheduled at {time_string}")

# Function to remove a scheduled task
def remove_task(command):
    """Remove a task from the schedule."""
    if command in scheduled_tasks:
        schedule.cancel_job(scheduled_tasks[command])
        del scheduled_tasks[command]
        print(f"Task '{command}' has been removed from the schedule")
    else:
        print(f"No task found for command '{command}'")

# Monitor system memory and run tasks if memory usage exceeds the threshold
def monitor_memory_threshold():
    """Monitor memory usage and run memory optimization tasks if threshold is exceeded."""
    memory_info = psutil.virtual_memory()
    if memory_info.percent > 80:  # Example threshold
        print(f"Memory usage is high: {memory_info.percent}%. Running memory optimization task.")
        execute_predefined_command('optimize_memory')

# Continuously run scheduled tasks and monitor system resources
def run_scheduled_tasks():
    """Run all scheduled tasks and monitor system resources."""
    while True:
        # Run any pending tasks scheduled with schedule library
        schedule.run_pending()

        # Monitor system memory and trigger any condition-based tasks
        monitor_memory_threshold()

        # Sleep for a short duration before checking again
        time.sleep(1)

# Example function to execute commands (should be replaced with your actual command execution logic)
def execute_predefined_command(command):
    """Placeholder for executing commands."""
    print(f"Executing command: {command}")

# Start task scheduler in a separate thread so it runs continuously
def start_task_scheduler():
    task_scheduler_thread = threading.Thread(target=run_scheduled_tasks)
    task_scheduler_thread.daemon = True  # Allow the thread to be killed when the main program exits
    task_scheduler_thread.start()

if __name__ == '__main__':
    # Example of scheduling a task
    schedule_task('optimize_memory', '23:00')  # Schedule a memory optimization task at 11 PM

    # Start the task scheduler
    start_task_scheduler()

    # Keep the main program running to allow the scheduler to work
    while True:
        time.sleep(10)
