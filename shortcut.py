#!/usr/bin/env python3
#Dylan Aguirre, 10/21/25

import os, pathlib, subprocess


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


def create_symlink(userInput:str,homeDesktop:str) -> None:
    options = find(userInput)
    if len(options) == 0: #No results returned
        print("No such filename!")
        return
    
    if len(options) == 1: #One option
        filepath = options[0]
    else: #More than one option
        filepath = select_option(options,userInput)

    os.symlink(filepath,homeDesktop)
    print(filepath+" is linked to "+homeDesktop)



def delete_symlink(homeDesktop:str):
    count = 1 #Starts at one for clarity of user
    #Generate list of all symlinks in home dir
    symLinks = symlink_report(homeDesktop)
    for line in symLinks:
        line = line.split()
        print(count+line[len(line)-1])
        count += 1
    #Select symlink
    userInput = int(input("Select symlink to delete (1-"+str(len(symLinks))+")"))-1
    #Delete symlink
    lineTokens = symLinks[userInput].split()
    os.remove(homeDesktop+lineTokens[len(lineTokens)-1])
    pass


def symlink_report(homeDesktop:str) -> list:
    symList = []
    #List all files in home dir
    lsOutput = subprocess.run(["ls","-la",homeDesktop], capture_output=True).stdout.decode()
    #Check if each file is a symlink
    for line in lsOutput.strip().split("\n"):
        #If symlink, add to list
        if "->" in line:
            symList.append(line)
    #Return list of symlinks
    return symList


def generate_report(homeDesktop:str) -> None:
    #Get report
    symList = symlink_report(homeDesktop)
    #Print report in nice format
    for line in symList:
        print(line)
    print("Total symlinks = "+str(len(symList)))


def main():
    homeDesktop = str(pathlib.Path.home())+ ("\\Desktop\\" if os.name == 'nt' else "/Desktop/")
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(os.getcwd())
        try:
            userInput = int(input("[1] Create Symbolic Link\n[2] Delete Symbolic Link\n[3] Generate Symbolic Link report\n[4] Quit\n>: "))
        except:
            print("Error! invalid selection")

        if userInput == 1: #Create symlink
            fileInput = input("Enter filename to link: ")
            create_symlink(fileInput,homeDesktop)
        elif userInput == 2: #Delete symlink
            delete_symlink(homeDesktop)
        elif userInput == 3: #symlink report
            generate_report(homeDesktop)
        elif userInput == 4: #Quit
            break
        else: #Number out of range
            print("Error! invalid selection")

        input("Press enter to continue...")

main()