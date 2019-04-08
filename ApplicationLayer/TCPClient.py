# coding:utf-8
# TCP 客户端

from socket import socket, AF_INET, SOCK_STREAM
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
# 多传回一条欢迎信息
print(clientSocket.recv(1024).decode('utf-8'))
while True:
    sentence = input('input: ').encode('utf-8')
    clientSocket.send(sentence)
    if sentence == b'bye':
        break
    message = clientSocket.recv(1024)
    print(message.decode('utf-8'))

clientSocket.close()
