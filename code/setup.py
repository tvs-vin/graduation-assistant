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
    else:
        database = sqlite3.connect(config["db_location"])
        

def main(
    databaseOverwrite: Optional[bool] = False,
    
    ):
    print('Running setup')
    databaseSetup(databaseOverwrite)
    
main()