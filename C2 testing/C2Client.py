import socket as Socket

def build_socket(sockType):
    serverSock = Socket.socket(Socket.AF_INET,sockType)
    return serverSock

def convert_to_bits(toSend:str):
    bitsOut = ""
    for letter in toSend:
        bitsOut += format(ord(letter),"08b")
    return bitsOut

def main():
    # udpSock = build_socket(Socket.SOCK_DGRAM)
    # tcpSock = build_socket(Socket.SOCK_STREAM)

    toSend = input("Message to send: ").strip()
    print(convert_to_bits(toSend))


main()