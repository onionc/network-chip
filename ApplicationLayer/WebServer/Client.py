# coding:utf-8
# HTTP客户端。 格式：client.py server_host server_port filename

from socket import socket, AF_INET, SOCK_STREAM
import sys

args = sys.argv[1:]
if len(args) != 3:
    print(r"（参数不足） 格式：.\client.py server_host server_port filename")
    exit()

host, port, filename = args

# 创建Socket, 建立连接
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((host, int(port)))

# 发送请求
request = f"GET {filename} HTTP/1.1\r\n\r\n"
clientSocket.send(request.encode())

# 接收响应数据
while True:
    response = clientSocket.recv(1024)
    # 无数据则退出
    if not response:
        break
    print(response.decode(), end='')

clientSocket.close()