#!/bin/bash

# Set SPI 
sudo raspi-config nonint do_spi 0

# Install busio
pip install adafruit-blinka

# Install adafruit-circuitpython for MCP3008
pip install adafruit-circuitpython-mcp3xxx

# Github setting
github_repo_url="https://github.com/dominikalesniewska/greenmind-device-manager.git"
destination_folder="/home/pi/Documents"

temp_folder=$(mktemp -d)

# Clone repo
git clone $github_repo_url $temp_folder

# Check for success
if [ $? -eq 0 ]; then
    echo "Pobrano repozytorium z GitHuba."
else
    echo "Błąd podczas pobierania repozytorium z GitHuba. Sprawdź poprawność adresu URL i upewnij się, że git jest zainstalowany."
    exit 1
fi

# Move to destination
mv $temp_folder/* $destination_folder

# Check for success
if [ $? -eq 0 ]; then
    echo "Przeniesiono zawartość repozytorium do $destination_folder."
    cd $destination_folder
    nohup sudo python gui.py > /dev/null 2>&1 &
    echo "Program GUI uruchomiony w tle."
else
    echo "Błąd podczas przenoszenia zawartości repozytorium. Sprawdź uprawnienia do zapisu."
fi

# Start service path
service_file="/etc/systemd/system/start.service"

# Start service content
service_content="[Unit]\nDescription=Growbox\nAfter=network.target\n\n[Service]\nUser=pi\nWorkingDirectory=/home/pi/Documents/scripts\nExecStart=python start.py\nRestart=always\n\n[Install]\nWantedBy=multi-user.target\n"

# Create file
echo -e $service_content | sudo tee $service_file

# Reload daemon
sudo systemctl daemon-reload

# Turn on daemon
sudo systemctl enable start.service

# Start service
sudo systemctl start start.service
