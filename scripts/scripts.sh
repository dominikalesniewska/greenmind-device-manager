#!/bin/bash

# Ścieżka do wirtualnego środowiska
venv_path="/home/pi/Documents/scripts/venv/bin/activate"

# Uruchomienie wirtualnego środowiska
source "$venv_path"

# Ścieżka do skryptu Pythona
python_script="/home/pi/Documents/scripts/start.py"

# Uruchomienie skryptu Pythona
python "$python_script"

