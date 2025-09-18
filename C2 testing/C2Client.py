import socket as Socket
import time

WAITTIME = 0.001
PORT = 1234
HOST = "127.0.0.1"

def build_socket(sockType):
    serverSock = Socket.socket(Socket.AF_INET,sockType)
    return serverSock


def convert_to_bits(toSend:str):
    bitsOut = ""
    for letter in toSend:
        bitsOut += format(ord(letter),"08b")
    return bitsOut


def send_traffic(message:str):
    udpSock = build_socket(Socket.SOCK_DGRAM)

    binaryToSend = convert_to_bits(message)
    for bit in binaryToSend:
        if int(bit) == 0: #Tcp connect
            tcpSock = build_socket(Socket.SOCK_STREAM)
            tcpSock.connect((HOST,PORT))
            tcpSock.send(b"")
            tcpSock.close()
            time.sleep(WAITTIME)
        else: #Udp connect
            udpSock.sendto(b"",(HOST,PORT))
            time.sleep(WAITTIME)
    time.sleep(0.5)
    udpSock.sendto(b"END",(HOST,PORT))



def main():
    udpSock = build_socket(Socket.SOCK_DGRAM)

    while True:
        toSend = input("Message to send: ").strip()
        send_traffic(toSend)


main()