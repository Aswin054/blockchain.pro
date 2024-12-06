from cryptography.fernet import Fernet
import bcrypt
import hashlib
import os
import json

# Constants for encryption and password hashing
ENCRYPTION_KEY_FILE = 'encryption_key.key'
USER_DATA_FILE = 'users.json'
DATA_FILE = 'sensitive_data.json'

# Generate or load encryption key
def load_or_generate_key():
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(ENCRYPTION_KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    return Fernet(key)

# Encrypt sensitive data
def encrypt_data(fernet, data):
    return fernet.encrypt(data.encode()).decode()

# Decrypt sensitive data
def decrypt_data(fernet, encrypted_data):
    return fernet.decrypt(encrypted_data.encode()).decode()

# Hash passwords securely
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

# Verify password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password.encode())

# Register a new user
def register_user(username, password):
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as user_file:
            users = json.load(user_file)
    else:
        users = {}

    if username in users:
        print("Username already exists.")
        return False
    
    users[username] = hash_password(password)
    with open(USER_DATA_FILE, 'w') as user_file:
        json.dump(users, user_file)
    
    print(f"User {username} registered successfully.")
    return True

# Authenticate user
def authenticate_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        print("No registered users.")
        return False
    
    with open(USER_DATA_FILE, 'r') as user_file:
        users = json.load(user_file)
    
    if username in users and verify_password(users[username], password):
        print(f"User {username} authenticated successfully.")
        return True
    else:
        print("Authentication failed.")
        return False

# Save encrypted data
def save_sensitive_data(fernet, data):
    encrypted_data = encrypt_data(fernet, data)
    data_hash = hashlib.sha256(data.encode()).hexdigest()

    with open(DATA_FILE, 'w') as data_file:
        json.dump({'data': encrypted_data, 'hash': data_hash}, data_file)
    
    print("Sensitive data saved securely.")

# Load and verify sensitive data
def load_sensitive_data(fernet):
    if not os.path.exists(DATA_FILE):
        print("No sensitive data found.")
        return None
    
    with open(DATA_FILE, 'r') as data_file:
        stored_data = json.load(data_file)
    
    decrypted_data = decrypt_data(fernet, stored_data['data'])
    current_hash = hashlib.sha256(decrypted_data.encode()).hexdigest()

    if current_hash == stored_data['hash']:
        print("Data integrity verified.")
        return decrypted_data
    else:
        print("Data integrity check failed!")
        return None

def main():
    fernet = load_or_generate_key()

    while True:
        print("\nData Privacy and Security System")
        print("1. Register User")
        print("2. Login")
        print("3. Save Sensitive Data")
        print("4. Load Sensitive Data")
        print("5. Exit")
        
        choice = input("Select an option: ").strip()

        if choice == '1':
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            register_user(username, password)
        
        elif choice == '2':
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            if authenticate_user(username, password):
                print("Access granted.")
            else:
                print("Access denied.")

        elif choice == '3':
            if authenticate_user(input("Enter username: ").strip(), input("Enter password: ").strip()):
                data = input("Enter sensitive data to save: ").strip()
                save_sensitive_data(fernet, data)
        
        elif choice == '4':
            if authenticate_user(input("Enter username: ").strip(), input("Enter password: ").strip()):
                data = load_sensitive_data(fernet)
                if data:
                    print(f"Loaded Sensitive Data: {data}")
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
