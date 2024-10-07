import json
import os

# File to store user profiles
USER_PROFILES_FILE = "logs/user_profiles.json"

# Load existing user profiles from the JSON file
if os.path.exists(USER_PROFILES_FILE):
    with open(USER_PROFILES_FILE, 'r') as f:
        user_profiles = json.load(f)
else:
    user_profiles = {}

# Function to create or update a user profile
def update_user_profile(user, preference_key, preference_value):
    """
    Update the user profile with new preferences or commands.
    
    :param user: The username.
    :param preference_key: The preference or command key (e.g., 'theme', 'frequent_commands').
    :param preference_value: The preference value (e.g., 'dark_mode', ['open_browser', 'shutdown']).
    """
    if user not in user_profiles:
        user_profiles[user] = {"preferences": {}, "frequent_commands": []}

    # Update the user preference
    user_profiles[user]["preferences"][preference_key] = preference_value

    # Save the updated user profiles to the file
    with open(USER_PROFILES_FILE, 'w') as f:
        json.dump(user_profiles, f, indent=4)

    return f"User profile for '{user}' updated."

# Function to retrieve a user profile
def get_user_profile(user):
    """
    Retrieve the profile of a specific user.
    
    :param user: The username.
    :return: User profile data or a message if the profile doesn't exist.
    """
    if user in user_profiles:
        return user_profiles[user]
    return f"User profile for '{user}' not found."

# Function to add a frequent command to a user's profile
def add_frequent_command(user, command):
    """
    Add a frequent command to the user's profile.
    
    :param user: The username.
    :param command: The command to add to the user's frequent commands list.
    """
    if user not in user_profiles:
        user_profiles[user] = {"preferences": {}, "frequent_commands": []}

    if command not in user_profiles[user]["frequent_commands"]:
        user_profiles[user]["frequent_commands"].append(command)
        # Save the updated profiles to the file
        with open(USER_PROFILES_FILE, 'w') as f:
            json.dump(user_profiles, f, indent=4)
        return f"Command '{command}' added to frequent commands for user '{user}'."
    else:
        return f"Command '{command}' is already in the frequent commands list for user '{user}'."

# Function to get frequent command suggestions for a user
def suggest_frequent_commands(user):
    """
    Suggest frequently used commands for the user based on their profile.
    
    :param user: The username.
    :return: List of frequently used commands or a message if no frequent commands found.
    """
    if user in user_profiles and user_profiles[user]["frequent_commands"]:
        return f"Suggestions for '{user}': {', '.join(user_profiles[user]['frequent_commands'])}"
    return f"No frequent commands found for '{user}'."

# Function to clear a user's profile
def clear_user_profile(user):
    """
    Clear a user's profile, removing preferences and frequent commands.
    
    :param user: The username.
    :return: Confirmation message.
    """
    if user in user_profiles:
        del user_profiles[user]
        with open(USER_PROFILES_FILE, 'w') as f:
            json.dump(user_profiles, f, indent=4)
        return f"User profile for '{user}' has been cleared."
    return f"User profile for '{user}' not found."

# Example usage
if __name__ == "__main__":
    # Example: Update user profile
    print(update_user_profile("user1", "theme", "dark_mode"))

    # Example: Add frequent command
    print(add_frequent_command("user1", "open_browser"))

    # Example: Get user profile
    print(get_user_profile("user1"))

    # Example: Suggest frequent commands
    print(suggest_frequent_commands("user1"))

    # Example: Clear user profile
    print(clear_user_profile("user1"))
