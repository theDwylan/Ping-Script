import socket as Socket
import threading

EOF = False
LOCK = threading.Lock()
PORT = 1234
HOST = "localhost"

def handle_UDP(UDPsock,BinaryHolder:str):
    global EOF
    global LOCK
    while True:
        data, addr = UDPsock.recvfrom(1024)
        LOCK.acquire()
        if data != "END" and not EOF:
            BinaryHolder += "1"
        else: #Message complete. Terminate thread
            EOF = True
            break
        LOCK.release()

def handle_TCP(TCPsock,BinaryHolder:str):
    global EOF
    global LOCK
    while True:
        clientSock, clientAddr = TCPsock.accept()
        LOCK.acquire()
        if clientSock.recv(1024) != b"END" and not EOF:
            BinaryHolder += "0"
        else: #Message complete. Terminate thread
            EOF = True
            clientSock.close()
            break
        LOCK.release()
        clientSock.close()

def decode(BinaryString:str): #Convert the collected binary list into a string
    bitSet = ""
    message = ""
    for i in range(0,len(BinaryString)-1,8):
        message += chr(int(BinaryString[i:i+8],2))
    return message

def build_socket(sockType, host:str, socket:int):
    serverSock = Socket.socket(Socket.AF_INET,sockType)
    serverSock.setsockopt(Socket.SOL_SOCKET,Socket.SO_REUSEADDR,1)
    serverSock.bind((host,socket))
    return serverSock


def main():
    serverSocketTCP = build_socket(Socket.SOCK_STREAM,HOST,PORT)
    serverSocketTCP.listen(5)

    serverSocketUDP = build_socket(Socket.SOCK_DGRAM,HOST,PORT)

    while True:
        BinaryString = ""

        #This is receiving data
        udp_Thread = threading.Thread(target=handle_UDP,args=(serverSocketUDP,BinaryString)) #Handles ones
        tcp_Thread = threading.Thread(target=handle_TCP,args=(serverSocketTCP,BinaryString)) #Handles zeros
        threads = [udp_Thread,tcp_Thread]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print(decode(BinaryString)) #Prints what the client sent discretely

main()