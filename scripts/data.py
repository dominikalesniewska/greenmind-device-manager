import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import requests
import json
import os

def get_token(url, file_path):
	headers = {"Content-Type": "application/json"}
	
	try:
		with open(file_path, "r") as file:
			device_id = int(file.read().strip())
		
		data = {"device_id": device_id}
		body = json.dumps(data)
		
		response = requests.post(url, headers=headers, data=body)
		response.raise_for_status()
		response_json = json.loads(response.text)
		token = response_json.get("access_token")
		
		os.system("sudo chmod 666 /home/pi/Documents/scripts/token.txt")
		
		with open("/home/pi/Documents/scripts/token.txt", "w") as token_file:
			token_file.write(str(token))
		
	except (ValueError,FileNotFoundError, requests.exceptions.RequestException) as err:
		print("POST request failed:", err)

def read_token(token_path):
	with open(token_path, "r") as token_file:
		bearer_token = token_file.read().strip()
	
	return bearer_token 

def read_values(file_name):
	with open(file_name, "r") as file:
		real_values = []
		sensor_values = []
		
		for line in file:
			parts = line.split()
			
			if len(parts) >= 2:
				real_value = float(parts[0].replace(",", "."))
				real_values.append(real_value)
				
				value = float(parts[1].replace(",", "."))
				sensor_values.append(value)
	return real_values, sensor_values

def predict(value, real_value, sensor_value):
	n = len(real_value)
	mean_x = sum(real_value) / n
	mean_y = sum(sensor_value) / n

	numer = sum(
		(x - mean_x) * (y - mean_y) for x, y in zip(real_value, sensor_value)
	)
	denom = sum((x - mean_x) ** 2 for x in real_value)

	slope = numer / denom
	intercept = mean_y - slope * mean_x
	
	return (value - intercept) / slope

if __name__ == "__main__":
	token_url = "https://python-microservice-api.greenmind.site/request_token"
	file_path = "/var/lib/greenmind/device_id.txt"
	
	spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
	cs = digitalio.DigitalInOut(board.D5)
	mcp = MCP.MCP3008(spi, cs)
	
	chan_0 = AnalogIn(mcp, MCP.P0)
	chan_1 = AnalogIn(mcp, MCP.P1)
	chan_2 = AnalogIn(mcp, MCP.P2)
	chan_3 = AnalogIn(mcp, MCP.P3)
	
	url = "https://python-microservice-api.greenmind.site/devices/data"
	
	try:
		while True:
			get_token(token_url, file_path)
			bearer_token = read_token("/home/pi/Documents/scripts/token.txt")
			
			air_hum = chan_0.value
			temp = chan_1.value
			light = chan_2.value
			soil_hum = chan_3.value
			
			real_temp, sens_temp = read_values("temp.txt")
			real_hum, sens_hum = read_values("hig.txt")
			
			temp = round(predict(temp, real_temp, sens_temp), 1)
			air_hum = round(predict(air_hum, real_hum, sens_hum))
			soil_hum = round((1 - (soil_hum / 66000)) * 100)
			light = round((light / 51000) * 100)
			
			data = {
				"soil_hum": soil_hum,
				"light": light,
				"air_hum": air_hum,
				"temp": temp
			}
			
			headers = {
				"Authorization": f"Bearer {bearer_token}",
				"Content-Type": "application/json"
			}
			
			response = requests.post(url, json=data, headers=headers)
			
			print('working data.py')
			time.sleep(10)
			
	
	except KeyboardInterrupt:
		print("\nProgram terminated by the user.")
