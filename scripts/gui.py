import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import requests


API_URL = "https://python-microservice-api.greenmind.site/authorize_device"
DEVICE_ID_FILE_PATH = "/var/lib/greenmind/device_id.txt"


def save_device_id(device_id):
    directory = "/var/lib/greenmind"

    if not os.path.exists(directory):
        os.makedirs(directory, mode=0o700)

    subprocess.run(["sudo", "chmod", "7777", "/var/lib/greenmind"])

    try:
        with open(DEVICE_ID_FILE_PATH, "w") as file:
            file.write(str(device_id))
    except IOError as e:
        print(f"Error saving device ID: {e}")


def submit_code():
    code = code_entry.get()
    code = code.strip()
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(API_URL, json={"code": code}, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(data["device_id"])
            save_device_id(data["device_id"])
            messagebox.showinfo("Success", data.get("message"))
        else:
            messagebox.showerror("Error", "Invalid code. Try again?")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Request failed: {e}")


root = tk.Tk()
root.title("Raspberry Pi Device Pairing")
root.geometry("400x170")

label = tk.Label(root, text="Enter Code", font=("Helvetica", 20))
code_entry = tk.Entry(root, font=("Helvetica", 12), width=16, justify="center")
submit_button = tk.Button(
    root, text="Pair Device", command=submit_code, font=("Helvetica", 12)
)

label.pack(pady=10)
code_entry.pack(pady=10)
submit_button.pack(pady=10)

root.mainloop()
