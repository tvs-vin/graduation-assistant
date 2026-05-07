# graduation-assistant-docs

## Config file
Below contains every option for the config.json file, what they do, and what they can be set to
    

### gui | 1
This value is used to set the **mode** the **UI** will be in. 

By default it will be set to **1** (**true**). Set it to anything else for **CLI** mode.

### debug | 0
This value enables debugging to be **output** to the **terminal**.

By default it will be set to **0** (**false**). Set it to **1** (**True**) to enable.

### first_launch | 1
This value is used to indicate wether or not the **initial setup** has been **completed** properly.

If it is set to any number other than 1, init setup will not run.

### reset | 0
This value is used to reset the config file to its original values (*stored in config.default.json*).

Set this to **1** (**true**) to enable. When the program is launched it will copy the files correctly and set the value back to 0

### db_location | database/main.db
This value controls where to program will go to for the SQlite database it uses to **store** the **ID-Numbers** and the **audio files** that go with them.



## Data structure
