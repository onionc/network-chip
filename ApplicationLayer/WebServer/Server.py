# coding:utf-8
# Web 服务器 v1.0

from socket import socket, AF_INET, SOCK_STREAM
import re

host, port = '', 8005
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(2)
print(f"{host}:{port} ready to receive")
while True:
    connection, address = serverSocket.accept()
    print(f'new connection from {address}')
    request = connection.recv(1024)
    print(request)

    try:
        path = re.findall(r'^\w+ +/([^ ]*)', request.decode('utf-8'))[0]
    except Exception:
        path = None

    if path == 'home':
        response = """\
HTTP/1.1 200 OK

hello, network.
"""
    elif path == 'index':
        response = """\
HTTP/1.1 301 Move
Location: home

"""
    else:
        response = """\
HTTP/1.1 404 Not Found

<html>
<body><h2>404</h2></body>
</html>
"""

    connection.sendall(response.encode('utf-8'))
    connection.close()
serverSocket.close()