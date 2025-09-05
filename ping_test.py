#!/usr/bin/env python3
import subprocess
import os
import time

def user_Input():
    try:
        userInput = int(input("> "))
    except (KeyboardInterrupt):
        return KeyboardInterrupt
    except:
        print("Error! Invalid command!")

    return userInput

def retrieve_Gateway(): #Get default gateway. Assumes rocky linux
    output = subprocess.run("ip r",capture_output=True).stdout.decode().split()
    return output[2]


def main():
    #Clear terminal
    #Source: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
    os.system('cls' if os.name == 'nt' else 'clear')
    
    while True:
        print("1. Display the default gateway\n\
2. Test Local Connectivity\n\
3. Test Remote Connectivity\n\
4. Test DNS Resolution\n\
5. Exit/quit the script")
 
        #Input checking
        userInput = user_Input()

        match userInput:
            case 1: #Display the default gateway
                print(retrieve_Gateway())
            case 2: #Test local connectivity
                print()
            case 3: #Test remote connectivity
                print()
            case 4: #Test DNS resolution
                output = subprocess.run(args= "ping www.google.com")
                print()
            case 5: #Quit
                print("Quitting...")
                break
            case __: #Check for bad command
                print("Command not recognized!")
        time.sleep(1)
        


main()