import socket as Socket
import threading

EOF = False
LOCK = threading.Lock()

def handle_UDP(UDPsock,BinaryHolder):
    global EOF
    global LOCK
    while True:
        data, addr = UDPsock.recvfrom(1024)
        LOCK.acquire()
        if data != "END" and not EOF:
            BinaryHolder.append(1)
        else: #Message complete. Terminate thread
            EOF = True
            break
        LOCK.release()

def handle_TCP(TCPsock,BinaryHolder):
    global EOF
    global LOCK
    while True:
        clientSock, clientAddr = TCPsock.accept()
        LOCK.acquire()
        if clientSock.recv(1024) != b"END" and not EOF:
            BinaryHolder.append(0)
        else: #Message complete. Terminate thread
            EOF = True
            clientSock.close()
            break
        LOCK.release()
        clientSock.close()

def decode(BinaryList): #Convert the collected binary list into a string
    message = ""
    return message

def build_socket(sockType):
    serverSock = Socket.socket(Socket.AF_INET,sockType)
    serverSock.setsockopt(Socket.SOL_SOCKET,Socket.SO_REUSEADDR,1)
    serverSock.bind(("0.0.0.0",1234))
    return serverSock


def main():
    serverSocketTCP = build_socket(Socket.SOCK_STREAM)
    serverSocketTCP.listen(5)

    serverSocketUDP = build_socket(Socket.SOCK_DGRAM)

    while True:
        BinaryList = list()

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