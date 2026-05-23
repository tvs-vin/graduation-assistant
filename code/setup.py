#                   The main use of this code is to make that files and folders exists

# Imports

import sqlite3
import json
import os
import tkinter as tk
import pygame
import pygame._sdl2.audio as sdl2_audio

from typing import Optional


with open("config.json") as f:
    config = json.load(f)
    
class setupGUI():
    def __init__(self, config):
        self.config = config
        self.debug = config["debug"] == "1"

        self.root = tk.Tk()
        self.root.title("Grad Assist Setup")
        self.root.geometry("1200x1000")
        self.root.configure(bg=self.config["bg_color"])
        self.root.resizable(True, True)
        self.main_frame = tk.Frame(padx=20, pady=20, bg=self.config["bg_color"])
        self.main_frame.pack(fill='both', expand=True)
        
        self.gui_switch("main")
    
    def gui_clear(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def gui_switch(self, menu: str, sub_menu: Optional[str] = None):    
        if(menu == "main"):
            self.gui_clear()
            self.main_label = tk.Label(self.main_frame, text="Welcome to Grad Assist!", font=("Arial", 24), bg=self.config["bg_color"], fg=self.config["fg_color"]).pack(pady=20)
            self.main_option_text = tk.Text(self.main_frame, font=("Arial", 18), bg=self.config["bg_color"], fg=self.config["fg_color"])
            self.main_option_text.insert('1.0', "Some setup is still required. Please follow the instructions, and refere to the help guide if needed (WIP)")
            self.main_option_text.configure(width=50, height=5,)
            self.main_option_text.pack(pady=10)
            self.main_option_button = tk.Button(self.main_frame, text="Start Setup", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: self.gui_switch("scan_menus")).pack(pady=10)
            
    # NON gui specific tools
    
    def databaseSetup(self, overwrite): # Overwrite should only be used reseting program fully
        if(overwrite):
            os.remove(self.config["db_location"])
        database = sqlite3.connect(self.config["db_location"])
        if(self.debug):
            print('Database connected')
        database.execute('''CREATE TABLE IF NOT EXISTS students
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                student_id TEXT NOT NULL,
                UNIQUE(student_id))''')
        if(self.debug):
            print('Students table checked/created')
        database.execute('''CREATE TABLE IF NOT EXISTS audio
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                audio_data TEXT NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(student_id))''')
        if(self.debug):
            print('Audio table checked/created')
        database.execute("""CREATE TABLE IF NOT EXISTS photos
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                photo_data BLOB NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(student_id))""")
        if(self.debug):
            print('Photos table checked/created')
        database.close()
        if(self.debug):
            print('Database setup complete')
    
    def confg_reset(self):
        if(self.config["reset"] == "1"):
            with open("config.default.json", "r") as f:
                default_config = json.load(f)
                with open("config.json", "w") as f:
                    json.dump(default_config, f, indent=4)

    def audiosetup(self):
        if not os.path.exists(f"{self.config["db_folder"]}/audio"):
            os.makedirs(f"{self.config["db_folder"]}/audio")
        if not os.path.exists(f"{self.config["db_folder"]}/photos"):
            os.makedirs(f"{self.config["db_folder"]}/photos")

        if(self.config["debug"] == "1"):
            print('Audio and photo folders checked/created')
            
        if(self.config['gui'] == "1"):
            pass
        else:
            print("""
                CLI SETTUP - AUDIO INPUTS:\n
                """)
            
            audio_devices = self.get_audio_outputs()
            for n, device in enumerate(audio_devices):
                print(f"{n + 1}.) {device}")
                
            
    
    def get_audio_outputs(self):
        pygame.mixer.init()
        audio_devices = sdl2_audio.get_audio_device_names()
        return audio_devices

def main(
    databaseOverwrite: Optional[bool] = False,
    ):
    
    app = setupGUI(config)
    
    if(config["debug"] == "1"):
        print('Running setup')
    app.databaseSetup(databaseOverwrite)
    app.audiosetup()
    if(config['gui'] == "1"):
        if(config["debug"] == "1"):
            print('Starting GUI Settup screen')
        app.root.mainloop()
    app.confg_reset()

main()