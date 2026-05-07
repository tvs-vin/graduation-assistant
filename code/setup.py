#                   The main use of this code is to make that files and folders exists

# Imports

import sqlite3
import json
import os

from typing import Optional

with open("config.json") as f:
    config = json.load(f)

def databaseSetup(overwrite): # Overwrite should only be used reseting program fully
    if(overwrite):
        os.remove(config["db_location"])
    database = sqlite3.connect(config["db_location"])
    database.execute('''CREATE TABLE IF NOT EXISTS students
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT NOT NULL,
            UNIQUE(student_id))''')
    database.execute('''CREATE TABLE IF NOT EXISTS audio
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            audio_data TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(student_id))''')
    database.execute("""CREATE TABLE IF NOT EXISTS photos
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            photo_data BLOB NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(student_id))""")
    database.close

def confg_reset():
    if(config["reset"] == "1"):
        with open("config.default.json", "r") as f:
            default_config = json.load(f)
            with open("config.json", "w") as f:
                json.dump(default_config, f, indent=4)

def main(
    databaseOverwrite: Optional[bool] = False,
    
    ):
    if(config["debug"] == "1"):
        print('Running setup')
    databaseSetup(databaseOverwrite)
    confg_reset()
    
main()