import os
import subprocess

VARIABLES_FILE = "variables.py"

def main():
    if not os.path.exists(VARIABLES_FILE):
        print("Variables file not found. Launching credentials setup...")
        subprocess.run(["python3", "create_credentials.py"])  # Launch credential creation GUI
    else:
        print("Variables file found. Proceeding to main script...")
        subprocess.run(["python3", "main.py"])  # Launch the main program


if __name__ == "__main__":
    main()
