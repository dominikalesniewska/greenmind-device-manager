import os
import requests
import subprocess
import time
import psutil
import json

def check_internet():
	try:
		response = requests.get("https://www.google.com", timeout=5)
		return True
	except requests.ConnectionError:
		return False
		
def check_file_existence(file_path):
	return os.path.isfile(file_path)

def execute_gui():
	gui_process = subprocess.Popen(["python", "/home/pi/Documents/scripts/gui.py"])
	
	return [gui_process]

def execute_scripts():
	data_process = subprocess.Popen(["python", "/home/pi/Documents/scripts/data.py"])
	task_process = subprocess.Popen(["python", "/home/pi/Documents/scripts/task.py"])
	
	return [data_process, task_process]

def disconnect_scripts(processes):
	for process in processes:
		process.terminate()
		process.wait()
	
if __name__ == "__main__":
	processes = []
	file_path = "/var/lib/greenmind/device_id.txt" #478
	
	while True:
		if check_internet():
			if check_file_existence(file_path):
				if "data" not in str(processes) and "task" not in str(processes):
					disconnect_scripts(processes)
					processes = execute_scripts()
					'''
			elif "gui" not in str(processes):
				disconnect_scripts(processes)
				processes = execute_gui()'''
		else:
			print("Lost internet connection")
			if processes:
				disconnect_scripts(processes)
				processes = []	
		
		time.sleep(5)
