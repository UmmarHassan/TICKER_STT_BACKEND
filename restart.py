import subprocess
import time

while True:
    subprocess.run(["restart_celery.bat"], shell=True)
    time.sleep(420)  # Sleep for 10 minutes (600 seconds)
