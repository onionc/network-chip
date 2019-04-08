# coding:utf-8
# TCP 服务器端

from socket import socket, AF_INET, SOCK_STREAM
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(4)
print("the server is ready to receive")
while True:
    connectionSocket, addr = serverSocket.accept()
    print(f'new connection from {addr}')
    connectionSocket.send(b'Welcome')

    while True:
        sentence = connectionSocket.recv(1024)
        print(f"received {sentence}., from {addr}")
        if sentence == b'bye':
            break
        message = sentence.upper()
        connectionSocket.send(message)

    connectionSocket.close()
serverSocket.close()