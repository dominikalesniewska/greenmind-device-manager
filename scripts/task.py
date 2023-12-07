import RPi.GPIO as GPIO
import time
import os
import requests
import subprocess

pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)

def read_token(token_path):
	with open(token_path, "r") as token_file:
		bearer_token = token_file.read().strip()
	
	return bearer_token 

def put_request(url, answer, status, bearer_token):
	headers = {
		"Authorization": f"Bearer {bearer_token}",
		"Content-Type": "application/json"
	}
	data = {
		"status": status,
		"task_id": answer.get("task_id")
	}
	
	response = requests.put(url, headers=headers, json=data)

if __name__ == "__main__":
	get_url = "https://python-microservice-api.greenmind.site/devices/tasks"
	put_url = "https://python-microservice-api.greenmind.site/devices/tasks/update"
	
	while True:
		if os.path.isfile("/home/pi/Documents/scripts/token.txt"):
			bearer_token = read_token("/home/pi/Documents/scripts/token.txt")
			
			header = {
				"Authorization": f"Bearer {bearer_token}"
			}
			
			response = requests.get(get_url, headers=header)
			if response.status_code == 200:
				answer = response.json()[0]
				
				if answer.get("task_number") == 0:
					put_request(put_url, answer, 1, bearer_token)
					GPIO.output(pin, GPIO.HIGH)
					
					time.sleep(1)
					
					GPIO.output(pin, GPIO.LOW)
					put_request(put_url, answer, 2, bearer_token)
				
				elif answer.get("task_number") == 1:
					put_request(put_url, answer, 2, bearer_token)
					subprocess.run("sudo rm /var/lib/greenmind/device_id.txt", shell=True, check=True)
			
		else:
			print("there is no file")
			
		print('working task.py')
		time.sleep(10)
		
	GPIO.cleanup()

