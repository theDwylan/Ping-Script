#!/usr/bin/env python3
#Dylan Aguirre, 10/21/25

import os, pathlib


#The find() func framework was found here 
#https://stackoverflow.com/questions/1724693/find-a-file-in-python
def find(name:str) -> list: 
    if os.name == "nt":
        rootDir = "C:\\"
    else:
        rootDir = "/"

    output = []
    for root, dirs, files in os.walk(rootDir):
        if name in files:
            output.append(os.path.join(root, name))
    return output


def select_option(options:list, filename:str) -> str: #Selects file from a list of options
    count = 1 #Added 1 for ease of reading
    print(f'Multiple options for filename "{filename}" were found')
    for option in options: #Display each option
        print(f"[{count}] {option}")
    while True:
        try:
            userInput = int(input(f"Choose file (1-{count}): "))
        except: #Typo/Wrong input handling
            print("Error! Invalid command")
        if userInput > count: #Out of bounds handling
            print("Error! Invalid option")
        else:
            return options[userInput-1]


def create_symlink(userInput:str):
    options = find(userInput)
    if len(options) == 0: #No results returned
        print("No such filename!")
        return
    
    if len(options) == 1: #One option
        filepath = options[0]
    else: #More than one option
        filepath = select_option(options,userInput)

    os.symlink(filepath,pathlib.Path.home())
    print(filepath+" is linked to "+str(pathlib.Path.home()))



def delete_symlink(userInput:str):
    #Generate list of all symlinks in home dir
    #Select symlink
    #Delete symlink
    pass


def symlink_report() -> list:
    symList = []
    #List all files in home dir
    #Check if each file is a symlink
    #If symlink, add to list
    #Return list of symlinks
    return symList


def generate_report():
    #Get report
    #Print report in nice format
    pass


def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(os.getcwd())
        try:
            userInput = int(input("[1] Create Symbolic Link\n[2] Delete Symbolic Link\n[3] Generate Symbolic Link report\n[4] Quit\n>: "))
        except:
            print("Error! invalid selection")

        if userInput == 1 or userInput == 2:
            fileInput = input("Enter filename to link: ")

        if userInput == 1: #Create symlink
            create_symlink(fileInput)
        elif userInput == 2: #Delete symlink
            pass
        elif userInput == 3: #symlink report
            pass
        elif userInput == 4: #Quit
            break
        else: #Number out of range
            print("Error! invalid selection")

        input("Press enter to continue...")

main()