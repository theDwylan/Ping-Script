#!/usr/bin/env python3
#Dylan Aguirre, 10/21/25

import os, pathlib


#The find() func was found here 
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


def select_option(options:list) -> str: #Selects file from a list of options
    count = 1 #Added 1 for ease of reading
    for option in options: #Display each option
        print(f"[{count}] {option}")
    while True:
        try:
            userInput = int(input("Choose file: "))
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
    
    if len(options) == 1: #One option thus link
        filepath = options[0]
    else: #More than one choice
        filepath = select_option(options)

    os.symlink(filepath,pathlib.Path.home())
    print(filepath+" is linked to "+str(pathlib.Path.home()))



def delete_symlink(userInput:str):
    pass


def symlink_report():
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