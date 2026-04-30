#                               The starter file for the program. 
#
#   This intended use of this is to launch the main UI, then go into the respective python scripts
#

# Imports

import json
import subprocess 
import sys

# sets vars

with open("config.json") as f:
    config = json.load(f)
    

# defs

def main() -> None:
    print('Starting Grad Assist')
    
    # Startup checks
    
    if(config["first_launch"] == 1):
        subprocess.run([sys.executable, "code/setup.py"])
    

# runs the program

main()