#!/usr/bin/env python3
#Dylan Aguirre, 9/5/25
import subprocess
import os
import time
import netifaces

def user_Input(): #Basic input checking
    try:
        userInput = input("> ")
        userInput = int(userInput)
        return userInput
    except(KeyboardInterrupt):
        raise KeyboardInterrupt
    except:
        print("Error! Invalid command!")
        raise SyntaxError

def retrieve_Gateway():
    return str(netifaces.gateways()["default"][2][0])
    # output = subprocess.run("ip r",capture_output=True).stdout.decode().split()
    # return output[2]

def ping_out(ip:str): #Checks for operating system type and prints returncode result
    if(os.name == "nt"): #Windows
        output = subprocess.run("ping "+str(ip),capture_output=True)
    else: #Linux/Mac
        output = subprocess.run(["ping","-c","4",str(ip)],capture_output=True)
    if(output.returncode == 0):
        print("Successful ping!")
    else:
        print("Ping failure!")

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

        if user_Input == 1: #Display the default gateway
            print(retrieve_Gateway())
        elif user_Input == 2: #Test local connectivity
            ping_out(retrieve_Gateway())
        elif user_Input == 3: #Test remote connectivity
            ping_out("129.21.3.17")
        elif user_Input == 4: #Test DNS resolution
            ping_out("www.google.com")
        elif user_Input == 5: #Quit
            print("Quitting...")
            break
        else: #Check for bad command
            print("Command not recognized!")
        input("\nPress enter to continue... ")


main()