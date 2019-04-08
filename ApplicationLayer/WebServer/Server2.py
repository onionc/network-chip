# coding:utf-8
# Web 服务器 v1.1 打开文件响应

from socket import socket, AF_INET, SOCK_STREAM

host, port = '', 8005
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(2)
print(f"{host}:{port} ready to receive")
while True:
    connection, address = serverSocket.accept()
    print(f'new connection from {address}')

    try:
        request = connection.recv(1024)
        print(request)
        # 获取文件名，并读取数据
        filename = request.split()[1][1:]
        with open(filename, encoding='utf-8') as f:
            outputdata = f.read()
        # 发送HTTP响应头
        header = b"HTTP/1.1 200 OK\r\n\r\n"
        connection.send(header)
        print(outputdata)

        # 这里发送数据没必要用单字符发，经验证直接send/sendall都会保证数据传输
        # for i in range(0, len(outputdata)):
        #     print(f"send:{outputdata[i]}")
        #     connection.send(outputdata[i].encode())
        connection.send(outputdata.encode())

    except Exception as e:
        print(e)
        header = b"HTTP/1.1 404 Not Found\r\n\r\n"
        connection.send(header)

    connection.close()
serverSocket.close()