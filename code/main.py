#                       The main program | Should run because of start.py

# Imports

import os
import sys
import json
import sqlite3
from time import sleep
import tkinter as tk
from tkinter import messagebox

with open("config.json", "r") as f:
    config = json.load(f)

class GradAssist:    
    def __init__(self):
        with open("config.json", "r") as f:
            self.config = json.load(f)
        
        if(self.config["gui"] == "1"):
            self.gui = True
        else:
            self.gui = False
        if(self.config["debug"] == "1"):
            self.debug = True
        else:
            self.debug = False
            
        if(self.gui):
            self.root = tk.Tk()
            self.root.title("ID Scanner System - TVS Vin")
            self.root.geometry("1000x800")
            self.root.resizable(False, False)
            self.main_frame = tk.Frame(padx=20, pady=20, bg=self.config["bg_color"])
            self.main_frame.pack(fill='both', expand=True)
        else:
            if(self.debug):
                print('Welcome to GradAssist! Running in console mode.')
        
        if(self.debug):
            print("Connecting to SQLite Database...")
        
        self.conn = sqlite3.connect(self.config["db_location"])
        self.cursor = self.conn.cursor()
        
        if(self.debug):
            print("Connected to database successfully.")
    
    
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
        
    
    def sq_fetchall(self, id):
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
            return string
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
    
    
    # Tools
    
    
    def quit(self): #safely quits the program
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
    else:
        app.mainloop()
    
# runs the script

main()