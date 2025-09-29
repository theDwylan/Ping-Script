#!/usr/bin/env python3
#Dylan Aguirre, 9/29/25

import netifaces
import socket
import os
import subprocess

def get_network_info(networkInfo:list):
    networkInfo[0] = socket.getfqdn()

def get_os_info(OSInfo:list):
    pass

def get_hardware_info(hardwareInfo:list):
    pass

def main():
    #Clear terminal
    #Print date

    networkInfo = [] #[Hostname,Domain suffix, ipv4 address, gateway, netmask, Primary dns, secondary dns]
    get_network_info(networkInfo)
    OSInfo = [] #[OSName, OSVersion, kernalVersion]
    get_os_info(OSInfo)
    hardwareInfo = [] #[diskSize, diskSpace, CPUModel, CPUNumber, CPUCoreCount, totalRAM, availableRAM]
    get_hardware_info(hardwareInfo)

    #Write to file

main()