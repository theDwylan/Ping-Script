#!/usr/bin/env python3
#Dylan Aguirre, 9/29/25

import netifaces,socket,os,platform,dns.resolver,calendar,shutil,psutil #netifaces, dns.resolver, and psutil need pip install
from datetime import date

def make_date_line()->str: #Assembles a clean formatted string
    properDateFormat = ""
    dateInfoTokens = str(date.today()).split("-")
    properDateFormat = str(calendar.month_name[int(dateInfoTokens[1])])+" "+dateInfoTokens[2]+", "+dateInfoTokens[0]
    return properDateFormat


def get_network_info(networkInfo:list) -> None:
    #Gets hostname and domain suffix
    fqdnTokens = socket.getfqdn().split(".")
    networkInfo[0] = fqdnTokens[0] #Host name
    for i in range(1,len(fqdnTokens)-1): #Rebuilds domain suffix
        networkInfo[1] += fqdnTokens[i]+"."
    networkInfo[1] = networkInfo[1][0:len(networkInfo[1])-1] #Removes extra "."

    #Gets IP info
    iface = netifaces.gateways()['default'][netifaces.AF_INET]
    networkInfo[3] = iface[0] #Gateway
    networkInfo[2] = netifaces.ifaddresses(iface[1])[netifaces.AF_INET][0]['addr'] #IP address
    networkInfo[4] = netifaces.ifaddresses(iface[1])[2][0]['netmask'] #Netmask

    #Get DNS info
    DNSservers = dns.resolver.Resolver().nameservers
    networkInfo[5] = DNSservers[0] #Primary DNS
    networkInfo[6] = DNSservers[1] #Secondary DNE


def get_os_info(OSInfo:list) -> None:
    OSInfo[0] = platform.system() #OS name
    OSInfo[1] = platform.version() #OS version
    OSInfo[2] = platform.release() #Kernel version


def get_hardware_info(hardwareInfo:list) -> None:
    #Get disk info
    totalDisk, usedDisk, freeDisk = shutil.disk_usage("/")
    hardwareInfo[0] = str(round(totalDisk / (1024**3)))+" GB"
    hardwareInfo[1] = str(round(freeDisk / (1024**3)))+" GB"
    hardwareInfo[2] = str(round((totalDisk-freeDisk) / (1024**3)))+" GB"

    #Get CPU info
    hardwareInfo[3] = platform.processor().split(",")[0]
    hardwareInfo[4] = psutil.cpu_count(logical=True)
    hardwareInfo[5] = psutil.cpu_count(logical=False)

    #Get RAM info
    ramMemory = psutil.virtual_memory() #Does not include SWAP
    hardwareInfo[6] = round(ramMemory.total / (1024**3))
    hardwareInfo[7] = round(ramMemory.available / (1024**3))


def format_output(networkInfo:list,OSInfo:list,hardwareInfo:list) -> str:
    spacingSize = int(30)
    return f"""System Report - {make_date_line()}

Device Information
{"Hostname:":{spacingSize}}{networkInfo[0]}
{"Gateway:":{spacingSize}}{networkInfo[1]}

Network Information
{"IP address:":{spacingSize}}{networkInfo[2]}
{"Gateway:":{spacingSize}}{networkInfo[3]}
{"Netmask:":{spacingSize}}{networkInfo[4]}
{"DNS1:":{spacingSize}}{networkInfo[5]}
{"DNS2:":{spacingSize}}{networkInfo[6]}

Operating System Information
{"Operating System:":{spacingSize}}{OSInfo[0]}
{"OS Version:":{spacingSize}}{OSInfo[1]}
{"Kernel Version:":{spacingSize}}{OSInfo[2]}

Storage Information
{"System Drive Total:":{spacingSize}}{hardwareInfo[0]}
{"System Drive Used:":{spacingSize}}{hardwareInfo[2]}
{"System Drive Free:":{spacingSize}}{hardwareInfo[1]}

Processor Information
{"CPU Model:":{spacingSize}}{hardwareInfo[3]}
{"Number of Processors:":{spacingSize}}{hardwareInfo[4]}
{"Number of Cores:":{spacingSize}}{hardwareInfo[5]}

Memory Information
{"Total RAM:":{spacingSize}}{hardwareInfo[6]}
{"Available RAM:":{spacingSize}}{hardwareInfo[7]}
"""

def main():
    #Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    networkInfo = [""] * 7 #[Hostname ,Domain suffix, ipv4 address, gateway, netmask, Primary dns, secondary dns]
    get_network_info(networkInfo)
    OSInfo = [""] * 3 #[OSName, OSVersion, kernalVersion]
    get_os_info(OSInfo)
    hardwareInfo = [""] * 8 #[diskSize, diskSpace, diskUsed, CPUModel, CPUNumber, CPUCoreCount, totalRAM, availableRAM]
    get_hardware_info(hardwareInfo)

    output = format_output(networkInfo,OSInfo,hardwareInfo)

    #Print output
    print(output)

    #Write to file
    home = os.path.expanduser("~")
    filename = networkInfo[0]+"_system_report.log"
    filename = os.path.join(home, filename)
    with open(filename,"w") as logFile:
        logFile.write(output)


main()