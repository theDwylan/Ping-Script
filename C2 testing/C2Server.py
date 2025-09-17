import socket as Socket
import threading

EOF = False
LOCK = threading.Lock()
PORT = 1234
HOST = "127.0.0.1"

def handle_UDP(UDPsock,BinaryHolder:list):
    global EOF
    global LOCK
    while not EOF:
        try:
            data, addr = UDPsock.recvfrom(1024)
        except Socket.timeout:
            continue
        print("Udp hit!")
        LOCK.acquire()
        if data != b"END" and not EOF:
            BinaryHolder.append("1")
            LOCK.release()
        else: #Message complete. Terminate thread
            EOF = True
            LOCK.release()
            break

def handle_TCP(TCPsock,BinaryHolder:list):
    global EOF
    global LOCK
    while not EOF:
        try:
            clientSock, clientAddr = TCPsock.accept()
        except Socket.timeout:
            continue
        print("Tcp hit!")
        LOCK.acquire()
        BinaryHolder.append("0")
        clientSock.close()
        LOCK.release()

def decode(BinaryList:list): #Convert the collected binary list into a string
    bitSet = ""
    message = ""
    binaryString = ""
    for i in range(len(BinaryList)):
        binaryString += BinaryList[i]
    for i in range(0,len(binaryString),8):
        message += chr(int(binaryString[i:i+8],2))
    return message

def build_socket(sockType, host:str, port:int):
    serverSock = Socket.socket(Socket.AF_INET,sockType)
    serverSock.setsockopt(Socket.SOL_SOCKET,Socket.SO_REUSEADDR,1)
    serverSock.settimeout(0.1)
    serverSock.bind((host,port))
    return serverSock


def main():
    global EOF
    serverSocketTCP = build_socket(Socket.SOCK_STREAM,HOST,PORT)
    serverSocketTCP.listen(5)

    serverSocketUDP = build_socket(Socket.SOCK_DGRAM,HOST,PORT)

    while True:
        BinaryList = []
        EOF = False

        #This is receiving data
        udp_Thread = threading.Thread(target=handle_UDP,args=(serverSocketUDP,BinaryList)) #Handles ones
        tcp_Thread = threading.Thread(target=handle_TCP,args=(serverSocketTCP,BinaryList)) #Handles zeros
        threads = [udp_Thread,tcp_Thread]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print(decode(BinaryList)) #Prints what the client sent discretely

main()