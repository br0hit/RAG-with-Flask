import subprocess
import requests
import time

subprocess.Popen(['python', 'question_answering_app.py'])
time.sleep(5)

try:
    response = requests.get('http://localhost:5001/stopServer')
    response.raise_for_status()  # Raise an exception for non-2xx status codes
    print("Server stopped successfully.")
except requests.exceptions.RequestException as e:
    print("Error stopping the server:", str(e))

print("The Python code reaches this line.")
