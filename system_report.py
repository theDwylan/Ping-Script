#!/usr/bin/env python3
#Dylan Aguirre, 9/29/25

import netifaces,socket,os,platform,dns.resolver,calendar,shutil,psutil
from datetime import date

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
    totalDisk, usedDisk, freeDisk = shutil.disk_usage("/")
    hardwareInfo[0] = str(round(totalDisk / (1024**3)))+" GB"
    hardwareInfo[1] = str(round(freeDisk / (1024**3)))+" GB"

    hardwareInfo[2] = platform.processor().split(",")[0]
    hardwareInfo[3] = psutil.cpu_count(logical=True)
    hardwareInfo[4] = psutil.cpu_count(logical=False)

    ramMemory = psutil.virtual_memory()
    hardwareInfo[5] = round(ramMemory.total / (1024**3))
    hardwareInfo[6] = round(ramMemory.available / (1024**3))

    print(hardwareInfo)


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