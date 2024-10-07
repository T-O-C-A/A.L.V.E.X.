from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
import base64
import json
import logging
import os

# Set up logging for command tracking and security events
logging.basicConfig(filename='logs/security_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Encryption settings
SALT = b'my_salt'  # Should be securely generated
KEY_LENGTH = 32  # AES-256 requires a 32-byte key

# Function to generate a key from a password
def generate_key(password):
    """Generate a 256-bit key from a password using scrypt key derivation."""
    return scrypt(password.encode(), SALT, KEY_LENGTH, N=2**14, r=8, p=1)

# Function to encrypt sensitive data
def encrypt_data(data, password):
    """Encrypt sensitive data using AES encryption."""
    key = generate_key(password)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())

    # Return base64-encoded ciphertext, nonce, and tag
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

# Function to decrypt sensitive data
def decrypt_data(encrypted_data, password):
    """Decrypt sensitive data encrypted using AES."""
    key = generate_key(password)
    encrypted_data = base64.b64decode(encrypted_data)

    # Extract nonce, tag, and ciphertext
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data.decode()
    except ValueError:
        return "Decryption failed. Invalid password or data integrity compromised."

# Function for logging user commands and security events
def log_command(command, user):
    """Log all commands and security events."""
    logging.info(f"User '{user}' executed command: {command}")

# Multi-Factor Authentication (MFA) Simulation
def request_mfa_code():
    """Simulate an MFA code generation and validation process."""
    mfa_code = "123456"  # In real life, this would be generated and sent to the user
    print(f"MFA Code sent: {mfa_code}")
    entered_code = input("Enter MFA Code: ")
    
    if entered_code == mfa_code:
        print("MFA authentication successful.")
        return True
    else:
        print("MFA authentication failed.")
        return False

# Function to handle user authentication (including optional MFA)
def authenticate_user(username, password, use_mfa=False):
    """Authenticate a user and optionally require MFA."""
    # For demonstration purposes, we'll assume a hardcoded username/password.
    # In a real-world application, you'd query a secure database.
    stored_password = "my_secure_password"

    if password == stored_password:
        if use_mfa:
            return request_mfa_code()
        return True
    else:
        return False

# Example function for encrypting and saving sensitive data to a file
def save_encrypted_file(filename, data, password):
    """Encrypt data and save it to a file."""
    encrypted_data = encrypt_data(data, password)
    
    with open(filename, 'w') as f:
        f.write(encrypted_data)
    print(f"Data saved to {filename} (encrypted)")

# Example function for loading and decrypting data from a file
def load_decrypted_file(filename, password):
    """Load and decrypt data from a file."""
    if not os.path.exists(filename):
        return "File not found."

    with open(filename, 'r') as f:
        encrypted_data = f.read()
    
    decrypted_data = decrypt_data(encrypted_data, password)
    return decrypted_data

# Example usage: Encrypting, saving, and decrypting data
if __name__ == "__main__":
    # Example of encrypting data
    password = "my_secure_password"
    sensitive_data = "This is some sensitive data."
    
    save_encrypted_file("encrypted_data.txt", sensitive_data, password)
    
    # Example of decrypting data
    decrypted_data = load_decrypted_file("encrypted_data.txt", password)
    print(f"Decrypted Data: {decrypted_data}")
    
    # Example of command logging
    log_command("open_browser", "user1")
    
    # Example of authentication with MFA
    if authenticate_user("user1", "my_secure_password", use_mfa=True):
        print("User authenticated successfully.")
    else:
        print("Authentication failed.")
