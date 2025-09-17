import socket as Socket
import threading

BINARYHOLDER = list()
EOF = False
LOCK = threading.Lock()

def handle_UDP(UDPsock):
    global EOF
    global BINARYHOLDER
    global LOCK
    while True:
        data, addr = UDPsock.recvfrom(1024)
        LOCK.acquire()
        if data != "END" and not EOF:
            BINARYHOLDER.append(1)
        else:
            EOF = True
            break
        LOCK.release()

def handle_TCP(TCPsock):
    global EOF
    global BINARYHOLDER
    global LOCK
    while True:
        clientSock, clientAddr = TCPsock.accept()
        LOCK.acquire()
        if clientSock.recv(1024) != b"END" and not EOF:
            BINARYHOLDER.append(0)
        else:
            EOF = True
            clientSock.close()
            break
        LOCK.release()
        clientSock.close()



def main():
    serverSocketTCP = Socket.socket(Socket.AF_INET,Socket.SOCK_STREAM)
    serverSocketTCP.setsockopt(Socket.SOL_SOCKET,Socket.SO_REUSEADDR,1)
    serverSocketTCP.bind(("0.0.0.0",1234))
    serverSocketTCP.listen(5)

    serverSocketUDP = Socket.socket(Socket.AF_INET,Socket.SOCK_DGRAM)
    serverSocketUDP.setsockopt(Socket.SOL_SOCKET,Socket.SO_REUSEADDR,1)
    serverSocketUDP.bind(("0.0.0.0",1234))

    udp_Thread = threading.Thread(target=handle_UDP,args=(serverSocketUDP,))
    tcp_Thread = threading.Thread(target=handle_TCP,args=(serverSocketTCP,))
    udp_Thread.start()
    tcp_Thread.start()

main()