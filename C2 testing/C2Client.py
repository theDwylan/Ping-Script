import socket as Socket

PORT = 1234
HOST = "localhost"

def build_socket(sockType):
    serverSock = Socket.socket(Socket.AF_INET,sockType)
    return serverSock

def convert_to_bits(toSend:str):
    bitsOut = ""
    for letter in toSend:
        bitsOut += format(ord(letter),"08b")
    return bitsOut


def main():
    udpSock = build_socket(Socket.SOCK_DGRAM)
    tcpSock = build_socket(Socket.SOCK_STREAM)

    toSend = input("Message to send: ").strip()
    binaryToSend = convert_to_bits(toSend)
    for bit in binaryToSend:
        if bit == 0: #Tcp connect
            tcpSock.connect((HOST,PORT))
            tcpSock.close()
        else: #Udp connect
            udpSock.sendto(b"",(HOST,PORT))


main()