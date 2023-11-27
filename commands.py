import subprocess
from datetime import datetime


commands = [
    "pwd",
    "id",
    "uname",
    "date",
    "hostname -i",
    "whoami",
    "ls"
]

def perform_command():
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Current date and time: {current_time}")
    print("-------------------------------")

    
    for cmd in commands:
        print(f"Running command: {cmd}")
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    
        print(result.stdout)

        # Print any errors
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
        print("-------------------------------")


run_commands()
