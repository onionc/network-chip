# coding:utf-8
# Web 服务器 v1.2 多线程版本

from socket import socket, AF_INET, SOCK_STREAM
import threading


def tcpLink(sock, addr):
    """ TCP 连接 """
    print(f'new connection from {addr}')
    try:
        request = sock.recv(1024)
        print(request)

        # 获取文件名，并读取数据
        filename = request.split()[1][1:]
        with open(filename, encoding='utf-8') as f:
            outputdata = f.read()
        # 发送HTTP响应头
        header = b"HTTP/1.1 200 OK\r\n\r\n"
        sock.send(header)
        # 发送数据
        sock.send(outputdata.encode())

    except Exception as e:
        print(f"error: {e}")
        header = b"HTTP/1.1 404 Not Found\r\n\r\n"
        sock.send(header)
    print(f"{addr} close.")
    sock.close()


host, port = '', 8005
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(4)
print(f"{host}:{port} ready to receive")
while True:
    connection, address = serverSocket.accept()

    # 新建函数处理TCP连接
    # tcpLink(connection, address)

    # 使用新线程来处理TCP连接
    t = threading.Thread(target=tcpLink, args=(connection, address))
    t.start()

serverSocket.close()