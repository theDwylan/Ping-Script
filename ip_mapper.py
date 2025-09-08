#!/usr/bin/env python3
import threading
import subprocess
import time

LOCK = threading.Lock()
RESULT = dict()

def ip_sort(a:str,b:str):
    aInt = a.split(".")[3]
    bInt = b.split(".")[3]
    if aInt > bInt:
        return -1
    elif aInt < bInt:
        return 1
    else:
        return 0

def ping_ip(ip:str):
    output = subprocess.run("ping "+ip,capture_output=True).returncode
    LOCK.acquire()
    RESULT[ip] = output
    LOCK.release()


def start_threads(userInput:list):
    networkBits = userInput[0]+"."+userInput[1]+"."+userInput[2]+"."
    for host in range(1,256):
        singleHost = networkBits+str(host)
        aThread = threading.Thread(target=ping_ip, args=(singleHost,))
        aThread.start()


def assemble_result():
    output = ""
    # sortedResult = dict(sorted(RESULT.items(), key=ip_sort))
    for key in RESULT.keys():
        if RESULT[key] == 0:
            ipResult = "There is a host at "+key+"\n"
            output += ipResult
    return output


def main():
    userInput = input("Enter ip range\n>: ").split(".") #Only works for /24
    start_threads(userInput)
    while len(RESULT) < 255:
        time.sleep(1)
    # print(RESULT)
    print(assemble_result())

main()