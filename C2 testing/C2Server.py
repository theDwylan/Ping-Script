import socket as Socket
from socket import socket
import threading

#TODO look into multiple sources. Convert main binary list to dict with ip/binary pairs?

EOF = False
LOCK = threading.Lock()
LISTLOCK = threading.Lock()
HOSTDICT = dict()
PORT = 1234
HOST = "127.0.0.1"

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


def handle_TCP(TCPsock:socket,BinaryHolder:list,senderIp:list):
    global EOF
    global LOCK
    while not EOF: #Main loop
        try:
            clientSock, clientAddr = TCPsock.accept()
        except Socket.timeout:
            continue
        recv_client_list(clientAddr)
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
    clientSock.send(send_client_list(clientAddr).encode())
    clientSock.close()
    senderIp.append(clientAddr[0])




def decode(BinaryList:list): #Convert the collected binary list into a string
    message = ""
    binaryString = ""
    for i in range(len(BinaryList)):
        binaryString += BinaryList[i]
    for i in range(0,len(binaryString),8):
        message += chr(int(binaryString[i:i+8],2))
    return message


def recv_client_list(clientAddr:tuple):
    global LISTLOCK
    global HOSTDICT
    if clientAddr not in HOSTDICT.keys():
        LISTLOCK.acquire()
        HOSTDICT[clientAddr] = list()
        LISTLOCK.release()


def send_client_list(clientAddr:tuple) -> str: #Fetch queued commands and return
    global LISTLOCK
    global HOSTDICT
    with LISTLOCK:
        if len(HOSTDICT.get(clientAddr, [])) == 0: # type: ignore
            return "SLP"
        else:
            return HOSTDICT[clientAddr].pop(0)


def build_socket(sockType, host:str, port:int):
    serverSock = Socket.socket(Socket.AF_INET,sockType)
    serverSock.setsockopt(Socket.SOL_SOCKET,Socket.SO_REUSEADDR,1)
    serverSock.settimeout(0.1)
    serverSock.bind((host,port))
    return serverSock


def receive_traffic(serverSocketUDP:socket,serverSocketTCP:socket) -> str:
    BinaryList = []
    senderIp = []
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
    print(senderIp[0]+": "+output) #Prints what the client sent discretely
    return output


def main():
    global EOF

    serverSocketTCP = build_socket(Socket.SOCK_STREAM,HOST,PORT)
    serverSocketTCP.listen(5)
    serverSocketUDP = build_socket(Socket.SOCK_DGRAM,HOST,PORT)

    while True:
        receive_traffic(serverSocketUDP,serverSocketTCP)

main()