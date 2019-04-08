# coding:utf-8
# UDP 心跳 客户端，发送时间戳

from socket import socket, AF_INET, SOCK_DGRAM
import time


host, port = '127.0.0.1', 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(5)

while True:
    sequence_number = input("请输入序号: ")
    message = f"{sequence_number} {time.time()}".encode()
    clientSocket.sendto(message, (host, port))
    recv_data, serverAddress = clientSocket.recvfrom(1024)
    print(f"{recv_data.decode('utf-8')}")

clientSocket.close()
