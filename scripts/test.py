import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import requests
import json
import os

if __name__ == "__main__":
	spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
	cs = digitalio.DigitalInOut(board.D5)
	mcp = MCP.MCP3008(spi, cs)
	
	chan_0 = AnalogIn(mcp, MCP.P0)
	chan_1 = AnalogIn(mcp, MCP.P1)
	chan_2 = AnalogIn(mcp, MCP.P2)
	chan_3 = AnalogIn(mcp, MCP.P3)
	
	try:
		while True:
			air_hum = chan_0.value
			temp = chan_1.value
			light = chan_2.value
			soil_hum = chan_3.value
			
			print(air_hum)
			print(temp)
			print(light)
			print(soil_hum)
			
			time.sleep(10)
			
	
	except KeyboardInterrupt:
		print("\nProgram terminated by the user.")
