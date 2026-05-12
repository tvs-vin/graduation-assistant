#                       The main program | Should run because of start.py

# Imports

import os
import sys
import json
import sqlite3
import tkinter as tk
from typing import Optional
import pygame
import time
import threading

from PIL import Image, ImageTk
from time import sleep
from tkinter import messagebox, simpledialog, ttk

with open("config.json", "r") as f:
    config = json.load(f)

class GradAssist:    
    def __init__(self):
        
        # Config setup
        
        with open("config.json", "r") as f:
            self.config = json.load(f)
        
        self.temp_config = self.config
        
        if(self.config["gui"] == "1"):
            self.gui = True
        else:
            self.gui = False
        if(self.config["debug"] == "1"):
            self.debug = True
        else:
            self.debug = False
        
        # GUI Setup
        
        if(self.gui):
            self.__initgui__()
            
        else:
            if(self.debug):
                print('Welcome to GradAssist! Running in console mode.')
        
        if(self.debug):
            print("Connecting to SQLite Database...")
        
        self.conn = sqlite3.connect(self.config["db_location"])
        self.cursor = self.conn.cursor()
        
        if(self.debug):
            print("Connected to database successfully.")
        
        # Audio player
        
        self.mixer = pygame.mixer
        self.mixer.init()
    
    
    # Menus - CLI
    
    
    def mainloop(self): # mainloop for CLI mode
        welcome_text = R"""
▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
▐                                                           ▌
▐                                                           ▌
▐    _____               _             _   _                ▌
▐   / ____|             | |           | | (_)               ▌
▐  | |  __ _ __ __ _  __| |_   _  __ _| |_ _  ___  _ __     ▌
▐  | | |_ | '__/ _` |/ _` | | | |/ _` | __| |/ _ \| '_ \    ▌
▐  | |__| | | | (_| | (_| | |_| | (_| | |_| | (_) | | | |   ▌
▐   \_____|_|  \__,_|\__,_|\__,_|\__,_|\__|_|\___/|_| |_|   ▌
▐          /\           (_)   | |            | |            ▌
▐         /  \   ___ ___ _ ___| |_ __ _ _ __ | |_           ▌
▐        / /\ \ / __/ __| / __| __/ _` | '_ \| __|          ▌
▐       / ____ \\__ \__ \ \__ \ || (_| | | | | |_           ▌
▐      /_/    \_\___/___/_|___/\__\__,_|_| |_|\__|          ▌
▐                                                           ▌
▐                                                           ▌
▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌
        """
        print(welcome_text)
        print("Options:\n\n   1.) Scan ID\n   2.) Database Management\n   3.) Config\n   4.) Exit")
        choice = input("\nEnter your choice: ")
        if(choice == "1"): # Scan
            print("WIP")
            self.mainloop()
        elif(choice == "2"): # Database Management
            self.db_menu()
        elif(choice == "3"): # Config
            self.config_menu()
        elif(choice == "4"): # Exit
            print("Exiting...")
            self.quit()
        elif(choice == "-1"):
            command = input("Enter command to run: ")
            try:
                exec(command)
            except Exception as e:
                print(f"Error executing command | {e}")
            input("\nPress Enter to continue...\n")
            self.mainloop()
        else:
            print("Invalid choice. Please try again.")
            self.mainloop()
    
    def db_menu(self):
        print("Options:\n1.) Lookup ID \n2.) Add to database \n3.) Back to Main Menu")
        choice = input("\nEnter your choice: ")
        if(choice == "1"):
            id = input("Enter student ID: ")
            print(self.sq_fetchall(id))
            input("\nPress Enter to continue...\n")
        elif(choice == "2"):
            id = input("Enter student ID: ")
            exists = self.sq_exists(id)
            print("\n")
            if(exists):
                print(f"{self.sq_fetchall(id)}\n")
                print("Options: \n1.) Name \n2.) Audio Data \n3.) Photo Data")
                choice = input("What value to edit: ")
                if(choice == "1"):
                    new_name = input("Enter new name: ")
                    self.sq_raw(f"""UPDATE students SET name = '{new_name}' WHERE student_id = {id}""")
                elif(choice == "2"):
                    new_audio = input("Enter new audio data: ")
                    self.sq_raw(f"""UPDATE audio SET audio_data = '{new_audio}' WHERE student_id = {id}""")
                elif(choice == "3"):
                    new_photo = input("Enter new photo data: ")
                    self.sq_raw(f"""UPDATE photos SET photo_data = '{new_photo}' WHERE student_id = {id}""")
            else:
                name = input("Enter student name: ")
                self.sq_insert(id, 1, name)
                audio_data = input("Enter audio data (or leave blank): ")
                if(audio_data != ""):
                    self.sq_insert(id, 2, audio_data)
                photo_data = input("Enter photo data (or leave blank): ")
                if(photo_data != ""):
                    self.sq_insert(id, 3, photo_data)
        
        self.mainloop()    
    
    def config_menu(self):
        if(self.gui):
            pass
        else:
            print("""
Config: 
    1.) Reset to defaults
    2.) Change config.json values
    3.) Turn on GUI
    4.) Back to Main Menu
                """)
            choice = input("\nEnter your choice: ")
            if(choice == "1"): # Reset to defaults
                temp_config = self.config
                temp_config["reset"] = 1
                self.update_config(temp_config) 
                print("Config reset to defaults. Relaunch the program.")
                self.quit()
            elif(choice == "2"): # Change config.json values
                
                # Value index
                values_page_1 = {"1": "gui", "2": "debug", "3": "first_launch", "4": "reset", "5": "db_location"}
                
                print("""
~----------------Values----------------~
|                                      |
|   Note - CLI mode lets you set ANY   |
|   value, even invalid ones.          |
|                                      |
|   1.) gui                            |
|   2.) debug                          |
|   3.) first_launch                   |
|   4.) reset                          |
|   5.) db_location                    |
|                                      |
~--------------------------------------~

                    """)
                choice = input("\nEnter the value you want to change: ")
                print(f"\n{values_page_1[choice]} is currently set to {self.config[values_page_1[choice]]}")
                new_value = input(f"Enter new value for {values_page_1[choice]}: ")
                temp_config = self.config
                temp_config[values_page_1[choice]] = new_value
                self.update_config(temp_config)
                self.config_menu()
            elif(choice == "3"): # Turn on GUI
                temp_conf = self.config
                temp_conf["gui"] = "1"
                self.update_config(temp_conf)
                print("Relaunch the Program")
                self.quit()
            elif(choice == "4"): # Back to Main Menu
                self.mainloop()
    
    
    # SQLite 
    
    def sq_insert(self, id: str, table: int, value: str):
        try:
            if(table == 1): # students
                self.cursor.execute(f"""INSERT INTO students (student_id, name) VALUES ({id}, {value})""")
            elif(table == 2): # photos
                self.cursor.execute(f"""INSERT INTO audio (student_id, audio_data) VALUES ({id}, {value})""")
            elif(table == 3): # audios
                self.cursor.execute(f"""INSERT INTO photos (student_id, photo_data) VALUES ({id}, {value})""")
            self.conn.commit()
        except Exception as e:
            print(f"Error executing query | {e}")
    
    def sq_fetchall_raw(self, id):
        try:
            query = f"""SELECT
                students.name,
                students.student_id,
                audio.audio_data,
                photos.photo_data
            FROM
                students
            LEFT JOIN
                photos ON students.student_id = photos.student_id
            LEFT JOIN
                audio ON students.student_id = audio.student_id
            WHERE students.student_id = {id}"""
            
            results = self.cursor.execute(query)
            return results.fetchall()
        except Exception as e:
            print(f"Error executing query | {e}")   
            return []
    
    def sq_fetchall(self, id, giveraw: Optional[bool] = False):
        try:
            query = f"""SELECT
                students.name,
                students.student_id,
                audio.audio_data,
                photos.photo_data
            FROM
                students
            LEFT JOIN
                photos ON students.student_id = photos.student_id
            LEFT JOIN
                audio ON students.student_id = audio.student_id
            WHERE students.student_id = {id}"""
            
            results = self.cursor.execute(query)
            
            string = ""
            
            for row in results:
                if(row[0] is not None):
                    string += f"Name: {row[0]}\n"
                if(row[1] is not None):
                    string += f"Student ID: {row[1]}\n"
                if(row[2] is not None):
                    string += f"Audio Data: Exists\n"
                else:
                    string += f"Audio Data: Not Set\n"
                if(row[3] is not None):
                    string += f"Photo Data: Exists\n"
                else:
                    string += f"Photo Data: Not Set\n"
            if(giveraw == False):
                return string
            else:
                return results
        except Exception as e:
            print(f"Error executing query | {e}")
    
    def sq_raw(self, query):
        try:
            return_var = self.cursor.execute(query)
        except Exception as e:
            print(f"Error executing query | {e}")
    
    def sq_lookup(self, id):
        try:
            return_var = self.cursor.execute(f"""SELECT name FROM students
                        WHERE student_id = {id}""")
            var = return_var.fetchall()
            return var[0]
        except Exception as e:
            print(f"Error executing query | {e}")
    
    def sq_exists(self, id):
        try:
            query = f"""SELECT 1 FROM students WHERE student_id = {id}"""
            result = self.cursor.execute(query).fetchone()
            if result is not None:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error executing query | {e}")
    
    
    # GUI
    
    def __initgui__(self):
        self.root = tk.Tk()
        self.root.title("ID Scanner System - TVS-Vin")
        self.root.geometry("1200x1000")
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
            
            self.main_menu = tk.Label(self.main_frame, text=f"GradAssist V{self.config['version']}", font=("Arial", 24), bg=self.config["bg_color"], fg=self.config["fg_color"]).pack(pady=20)
            
            self.options_main_frame = tk.Frame(self.main_frame, bg=self.config["bg_color"])
            self.options_main_option_scan_mode = tk.Button(self.options_main_frame, text="Scan ID", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: self.gui_switch("scan_menus", "scan_main")).pack(pady=10)
            self.options_main_option_database_management = tk.Button(self.options_main_frame, text="Database Management", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: self.gui_switch("db_menu")).pack(pady=10)
            self.options_main_option_config = tk.Button(self.options_main_frame, text="Config", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: self.gui_switch("config_menu")).pack(pady=10)
            if(self.debug):
                self.options_main_option_activate_cli_loop = tk.Button(self.options_main_frame, text="Activate CLI Loop", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: self.mainloop()).pack(pady=10)
            self.options_main_option_exit = tk.Button(self.options_main_frame, text="Exit", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: self.quit()).pack(pady=10)
            self.options_main_frame.pack(pady=20)
        
        elif(menu == "scan_menus"):
            if(sub_menu == "scan_main"):
                self.gui_clear()

                self.scan_main_label = tk.Label(self.main_frame, text="Scan Mode", font=("Arial", 24), bg=self.config["bg_color"], fg=self.config["fg_color"]).pack(pady=20)

                self.scan_main_option_start_scan = tk.Button(self.main_frame, text="Start Scan", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: self.gui_switch("scan_menus", "scan_active")).pack(pady=10)
                self.scan_main_option_back_to_main_menu = tk.Button(self.main_frame, text="Back to Main Menu", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: self.gui_switch("main")).pack(pady=10)
            
            if(sub_menu == "scan_active"):
                self.gui_clear()
                
                self.scan_active_label = tk.Label(self.main_frame, text="Scan Mode", font=("Arial", 24), bg=self.config["bg_color"], fg=self.config["fg_color"]).pack(pady=20)

                image = self.gui_image()
                self.scan_active_image = tk.Label(self.main_frame, bg=self.config["bg_color"], image=image)
                self.scan_active_image.configure(image=image)
                self.scan_active_image.pack(pady=10)
                
                self.scan_active_name = tk.Label(self.main_frame, text="Please scan ID", font=("Arial", 18), bg=self.config["bg_color"], fg=self.config["fg_color"]).pack(pady=10)
                
                self.scan_active_scanbox_entry_var = tk.StringVar()
                self.scan_active_scanbox = tk.Entry(self.main_frame, font=("Arial", 18), fg=self.config["fg_color"], bg=self.config["bg_color"], textvariable=self.scan_active_scanbox_entry_var).bind('<Return>', self.scan_handler(self.scan_active_scanbox_entry_var.get()))
                
                
        elif(menu == "db_menu"):
            self.gui_clear()
            
            self.db_menu_label = tk.Label(self.main_frame, text="Database Management", font=("Arial", 24), bg=self.config["bg_color"], fg=self.config["fg_color"]).pack(pady=20)
            
            self.db_menu_option_lookup_id = tk.Button(self.main_frame, text="Lookup ID", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: print("WIP")).pack(pady=10)
            self.db_menu_option_edit_database = tk.Button(self.main_frame, text="Edit Database", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: print("WIP")).pack(pady=10)
            self.db_menu_option_back_to_main_menu = tk.Button(self.main_frame, text="Back to Main Menu", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: self.gui_switch("main")).pack(pady=10)
        
        elif(menu == "config_menu"):
            self.gui_clear()
            
            self.config_menu_label = tk.Label(self.main_frame, text="Config", font=("Arial", 24), bg=self.config["bg_color"], fg=self.config["fg_color"]).pack(pady=20)
            
            self.config_menu_option_reset_to_defaults = tk.Button(self.main_frame, text="Reset to Defaults", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: self.gui_tools(menu="config", tool="reset")).pack(pady=10)
            self.config_menu_option_change_config_values = tk.Button(self.main_frame, text="Change Config Values", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: print("WIP")).pack(pady=10)
            self.config_menu_option_turn_off_gui = tk.Button(self.main_frame, text="Turn off GUI (Relaunch Required)", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: self.gui_tools(menu="config", tool="gui_toggle")).pack(pady=10)
            self.config_menu_option_back_to_main_menu = tk.Button(self.main_frame, text="Back to Main Menu", font=("Arial", 18), bg=self.config["fg_color"], fg=self.config["bg_color"], command=lambda: self.gui_switch("main")).pack(pady=10)
    
    def scan_handler(self, student_id: Optional[str] = ""):
        if (student_id == ""):
            student_id = simpledialog.askstring(title="Please scan the ID now.", prompt="Scan the ID now.")
        
        if(self.debug):
            print(f"Scanned ID: {student_id}")
        results = self.sq_fetchall_raw(student_id)
        if results == []:
            if(self.debug):
                print("No results found for scanned ID.")
            messagebox.showerror("Error", "No results found for scanned ID.")
            return
        results_list = list(results) # 0: name 1: ID 2: audio data loc 3: photo data loc
        
        
        
    
    # Tools
    
    def gui_image(self, param: Optional[str] = "default"):
        if(param == "default"):
            pil_img = Image.open("images/def-cropped.jpeg")
            pil_img = pil_img.resize((400, 400))
            tk_img = ImageTk.PhotoImage(pil_img)
            return tk_img
        else:
            return ImageTk.PhotoImage(Image.open("images/def.png").resize((400, 400)))
    
    def gui_tools(self, menu: Optional[str], tool: Optional[str], param: Optional[str] = None):
        if(menu == "config"):
            if(tool == "reset"):
                temp_conf = self.config
                temp_conf["reset"] = "1"
                self.update_config(temp_conf)
                messagebox.showinfo("Config Reset", "Config reset to defaults. Relaunch the program.")
                self.quit()
            elif(tool == "gui_toggle"):
                temp_conf = self.config
                temp_conf["gui"] = "0"
                self.update_config(temp_conf)
                messagebox.showinfo("GUI Toggled", "GUI turned off. Relaunch the program.")
                self.quit()
        elif(menu == "scan"):
            pass
    
    def mixer_play(self, audio_path):
        if(os.path.exists(audio_path)):
            self.mixer.music.load(audio_path)
            self.mixer.music.play()
        elif(self.debug):
            print(f"Audio file not found at {audio_path}")
    
    def quit(self): #safely quits the program
        if(self.debug):
            print('Exitings...')
        self.conn.close()
        quit()
    
    def read_input(self, input):
        if(self.gui == True):
            print(input)
    
    def update_config(self, new_config):
        with open("config.json", "w") as f:
            json.dump(new_config, f, indent=4)
        with open("config.json", "r") as f:
            self.config = json.load(f)
    
def main():
    if(config["debug"] == "1"):
        print('starting main')
    app = GradAssist()
    if(app.gui == True):
        app.root.mainloop()
        app.quit()
    else:
        app.mainloop()
    
# runs the script

main()