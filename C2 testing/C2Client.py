import socket as Socket

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


def main():
    udpSock = build_socket(Socket.SOCK_DGRAM)

    while True:
        toSend = input("Message to send: ").strip()
        binaryToSend = convert_to_bits(toSend)
        for bit in binaryToSend:
            if int(bit) == 0: #Tcp connect
                tcpSock = build_socket(Socket.SOCK_STREAM)
                tcpSock.connect((HOST,PORT))
                tcpSock.send(b"")
                tcpSock.close()
            else: #Udp connect
                udpSock.sendto(b"",(HOST,PORT))
        udpSock.sendto(b"END",(HOST,PORT))


main()