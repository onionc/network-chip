# coding:utf-8
# UDP 心跳 客户端（监测端）

from socket import socket, AF_INET, SOCK_DGRAM
import time
import os

host, port = '127.0.0.1', 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(5)

while True:
    clientSocket.sendto(b'online', (host, port))

    time_s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    print(f"online list: {time_s}")
    # 接收数据
    while True:
        recv_data, serverAddress = clientSocket.recvfrom(1024)
        recv_data = recv_data.decode()
        if recv_data == 'over':
            # 传输完毕
            break
        print(f"{recv_data}")

    time.sleep(1)
    os.system("cls")

clientSocket.close()
