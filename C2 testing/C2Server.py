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


def main():
    serverSocketTCP = Socket.socket(Socket.AF_INET,Socket.SOCK_STREAM)
    serverSocketTCP.setsockopt(Socket.SOL_SOCKET,Socket.SO_REUSEADDR,1)
    serverSocketTCP.bind(("0.0.0.0",1234))
    serverSocketTCP.listen(5)

    serverSocketUDP = Socket.socket(Socket.AF_INET,Socket.SOCK_DGRAM)
    serverSocketUDP.setsockopt(Socket.SOL_SOCKET,Socket.SO_REUSEADDR,1)
    serverSocketUDP.bind(("0.0.0.0",1234))

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