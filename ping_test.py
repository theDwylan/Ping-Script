#!/usr/bin/env python
import subprocess
import os

def main():
    #Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    while True:
        print("1. Display the default gateway\n\
2. Test Local Connectivity\n\
3. Test Remote Connectivity\n\
4. Test DNS Resolution\n\
5. Exit/quit the script")
 
        #Input checking
        try:
            userInput = int(input("> "))
        except:
            print("Error! Invalid command!")

        match userInput:
            case 1:
                #Display the default gateway
                print()
            case 2:
                #Test local connectivity
                print()
            case 3:
                #Test remote connectivity
                print()
            case 4:
                #Test DNS resolution
                print()
            case 5:
                #Quit
                print("Quitting...")
                break
            case __:
                print("Command not recognized!")


main()