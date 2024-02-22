import subprocess
import time

ticker_process = None

while True:
    try:
        # Try to read the stored PID from the file
        try:
            with open("ticker.txt", "r") as pid_file:
                pid = pid_file.read()
        except FileNotFoundError:
            pid = None

        print(f"Stored PID: {pid}")

        if pid and ticker_process is not None:
            try:
                # Terminate the FastAPI process
                ticker_process.terminate()
                ticker_process.wait()  # Wait for the process to terminate

                print("Ticker process terminated.")
            except Exception as e:
                # Handle errors when terminating the process
                print(f"Error terminating FastAPI process: {e}")

        # Start the FastAPI application using subprocess.Popen
        ticker_process = subprocess.Popen(["python", "ticker.py"])

        time.sleep(3600)  # Sleep for 5 minutes (300 seconds)
    except Exception as e:
        # Handle other exceptions that may occur
        print(f"Error: {e}")
