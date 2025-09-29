#!/usr/bin/env python3
#Dylan Aguirre, 9/29/25

import netifaces
import socket
import os
import subprocess
import platform
import dns.resolver
from datetime import date
import calendar

def make_date_line()->str:
    properDateFormat = ""
    dateInfoTokens = str(date.today()).split("-")
    properDateFormat = str(calendar.month_name[int(dateInfoTokens[1])])+" "+dateInfoTokens[2]+", "+dateInfoTokens[0]
    return properDateFormat

def get_network_info(networkInfo:list) -> None:

    fqdnTokens = socket.getfqdn().split(".") #Gets hostname and domain suffix
    networkInfo[0] = fqdnTokens[0]
    for i in range(1,len(fqdnTokens)-1):
        networkInfo[1] += fqdnTokens[i]+"."
    networkInfo[1] = networkInfo[1][0:len(networkInfo[1])-1] #Removes extra "."

    iface = netifaces.gateways()['default'][netifaces.AF_INET]
    networkInfo[3] = iface[0]
    networkInfo[2] = netifaces.ifaddresses(iface[1])[netifaces.AF_INET][0]['addr']
    networkInfo[4] = netifaces.ifaddresses(iface[1])[2][0]['netmask']

    DNSservers = dns.resolver.Resolver().nameservers
    networkInfo[5] = DNSservers[0]
    networkInfo[6] = DNSservers[1]


def get_os_info(OSInfo:list) -> None:
    OSInfo[0] = platform.system()
    OSInfo[1] = platform.version()
    OSInfo[2] = platform.release()

def get_hardware_info(hardwareInfo:list) -> None:
    pass

def main():
    #Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    dateLine = make_date_line()


    networkInfo = [""] * 7 #[Hostname ,Domain suffix, ipv4 address, gateway, netmask, Primary dns, secondary dns]
    get_network_info(networkInfo)
    OSInfo = [""] * 3 #[OSName, OSVersion, kernalVersion]
    get_os_info(OSInfo)
    hardwareInfo = [""] * 7 #[diskSize, diskSpace, CPUModel, CPUNumber, CPUCoreCount, totalRAM, availableRAM]
    get_hardware_info(hardwareInfo)

    #Write to file

main()