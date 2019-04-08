# coding:utf-8
# UDP 服务器端

from socket import socket, AF_INET, SOCK_DGRAM
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("the server is ready to receive")
while True:
    print('waiting... ')
    message, clientAddress = serverSocket.recvfrom(2048)
    print(f"received {message}, from {clientAddress}")

    if message == b'bye':
        serverSocket.sendto(b'I see u.', clientAddress)
        break
    modifiedMessage = message.upper()
    serverSocket.sendto(modifiedMessage, clientAddress)
