import subprocess
import time

fastapi_process = None

while True:
    try:
        # Try to read the stored PID from the file
        try:
            with open("fastapi_pid.txt", "r") as pid_file:
                pid = pid_file.read()
        except FileNotFoundError:
            pid = None

        print(f"Stored PID: {pid}")

        if pid and fastapi_process is not None:
            try:
                # Terminate the FastAPI process
                fastapi_process.terminate()
                fastapi_process.wait()  # Wait for the process to terminate

                print("FastAPI process terminated.")
            except Exception as e:
                # Handle errors when terminating the process
                print(f"Error terminating FastAPI process: {e}")

        # Start the FastAPI application using subprocess.Popen
        fastapi_process = subprocess.Popen(["python", "model_api.py"])

        time.sleep(600)  # Sleep for 5 minutes (300 seconds)
    except Exception as e:
        # Handle other exceptions that may occur
        print(f"Error: {e}")
