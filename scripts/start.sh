#!/bin/bash

# Zawartość pliku start.service
service_content="[Unit]
Description=Uruchamianie mojego skryptu bashowego

[Service]
ExecStart=/home/pi/Documents/scripts/scripts.sh
Restart=always
User=pi

[Install]
WantedBy=multi-user.target"

# Tworzenie pliku start.service
echo "$service_content" | sudo tee /etc/systemd/system/start.service > /dev/null

# Przeładowanie systemd
sudo systemctl daemon-reload

# Włączenie i uruchomienie usługi
sudo systemctl enable start.service
sudo systemctl start start.service
