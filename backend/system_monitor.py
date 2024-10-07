import psutil
import time

# Function to monitor CPU usage
def monitor_cpu_usage():
    """
    Monitor the CPU usage percentage in real-time.
    :return: Current CPU usage as a percentage.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"CPU Usage: {cpu_usage}%"

# Function to monitor memory (RAM) usage
def monitor_memory_usage():
    """
    Monitor the current memory (RAM) usage.
    :return: Memory usage as a percentage and available memory in GB.
    """
    memory_info = psutil.virtual_memory()
    used_memory = memory_info.percent
    available_memory = memory_info.available / (1024 ** 3)  # Convert bytes to GB
    return f"Memory Usage: {used_memory}%, Available Memory: {available_memory:.2f} GB"

# Function to monitor disk usage for a specified partition
def monitor_disk_usage(disk="/"):
    """
    Monitor disk usage for a specified partition.
    :param disk: The disk partition to monitor (e.g., "/", "C:/").
    :return: Disk usage as a percentage and available disk space in GB.
    """
    disk_info = psutil.disk_usage(disk)
    used_disk = disk_info.percent
    available_disk = disk_info.free / (1024 ** 3)  # Convert bytes to GB
    return f"Disk Usage: {used_disk}%, Available Disk Space: {available_disk:.2f} GB"

# Function to suggest system optimizations based on resource usage
def suggest_system_optimizations():
    """
    Suggest system optimizations based on current resource usage.
    :return: List of suggested actions (e.g., optimize memory, free up disk space).
    """
    suggestions = []

    # Check CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > 80:
        suggestions.append("High CPU usage detected. Suggest closing unnecessary applications.")

    # Check memory usage
    memory_info = psutil.virtual_memory()
    if memory_info.percent > 80:
        suggestions.append("High memory usage detected. Suggest optimizing memory or closing unused programs.")

    # Check disk usage
    disk_info = psutil.disk_usage("/")
    if disk_info.percent > 80:
        suggestions.append("Low disk space available. Suggest freeing up disk space or deleting unused files.")

    if not suggestions:
        return "System resources are within normal usage."
    return suggestions

# Function to monitor all system resources periodically
def monitor_system_resources(interval=10):
    """
    Continuously monitor system resources (CPU, memory, and disk) at a specified interval.
    :param interval: Time interval (in seconds) between checks.
    """
    while True:
        cpu = monitor_cpu_usage()
        memory = monitor_memory_usage()
        disk = monitor_disk_usage()

        print(cpu)
        print(memory)
        print(disk)
        print("---------")

        time.sleep(interval)

# Example usage: Monitor system resources and suggest optimizations
if __name__ == "__main__":
    # Print current system resource usage
    print(monitor_cpu_usage())
    print(monitor_memory_usage())
    print(monitor_disk_usage("/"))

    # Suggest system optimizations based on current resource usage
    suggestions = suggest_system_optimizations()
    if isinstance(suggestions, list):
        for suggestion in suggestions:
            print(suggestion)
    else:
        print(suggestions)

    # Example: Continuously monitor system resources every 10 seconds
    # monitor_system_resources(interval=10)

def get_system_status():
    """
    Get the current CPU, memory, and disk usage.
    Returns a dictionary with the system status.
    """
    status = {
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }
    return status