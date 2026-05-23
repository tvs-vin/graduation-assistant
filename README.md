# graduation-assistant <img src=images/logo.png alt= "Graduation Assistant Logo" width=10% align="right">

A program that aims to make announcing names easier, modular, and usable by most 

# PLANNING

The program needs to accept input, and then translate that into a DB lookup to find the sound file. This should then be played out of the selected audio device. 

# TODO

- [x] Figure out main language
    - Python 3.13.5
- [X] Make datastructure
    - [x] SQLite 3, a built in package in python will be used
    - [X] Audio files and photos are stored as raw files in the database directory
    - [X] Still needs to be flushed out
- [ ] Decide feature-set
    - [ ] Make data
    - [ ] Easy import of data
        - [ ] CSV for names with their ID.
            - [ ] Figure out formating for it
            - [ ] Make function for it
        - [X] Audio files will be named the ID number
        - [X] Photo (*if used*) will be named with ID Number
- [ ] Make UI
    - [X] Basic style, not ment for public to see.
    - [X] Colors all configurable with config.json

## Configuration

Configuration will be handled by the file `config.json`

## Input

Input will be done with a standard **USB BARCODE SCANNER**. All code will assume it acts as such, as in the scanner inputs the data and then submits the data on its own

## Data Storage

Data is stored in 2 methods

### Database Directory

This can be changed in the config file, and is where the database files and other files will be storeed. It will have the **SQLite database** file in its **root**, with **2 subdirectories** for each **photos** and **audio**

#### Database (SQLite 3)

This is a fast way of storing a large dataset. It uses tables to store different values. In this use-case, it has 3 tablets that will be needed. "**students**", "**photos**", and "**audio**". 

## Audio routing

Audio is handled with Pygame, a python libary.