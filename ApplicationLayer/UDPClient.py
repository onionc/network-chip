# coding:utf-8
# UDP 客户端

from socket import socket, AF_INET, SOCK_DGRAM
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input("input: ").encode('utf-8')
clientSocket.sendto(message, (serverName, serverPort))
message, serverAddress = clientSocket.recvfrom(2048)
print(message.decode('utf-8'), "from ", serverAddress)
clientSocket.close()
