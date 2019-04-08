# coding:utf-8
# SMTP 邮件客户端

from socket import socket, AF_INET, SOCK_STREAM
import base64
import ssl

def tcp_send(cli, message, except_code):
    print("C: " + message)
    cli.send((message+'\r\n').encode())
    response = cli.recv(1024)
    response = response.decode()
    print("S: " + response)
    if response[:3] == str(except_code):
        return response
    raise Exception(response[:3])

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailServer = 'smtp.sina.cn'
mailPort = 587
# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, mailPort))
clientSocket.settimeout(5)
# 邮件服务器连接响应信息
response = clientSocket.recv(1024).decode()
print('S: ' + response)

if response[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response. 打招呼
heloCommand = 'EHLO Alice'
tcp_send(clientSocket, heloCommand, 250)

# TLS/SSL 加密传输
tcp_send(clientSocket, 'STARTTLS', 220)
clientSocket = ssl.wrap_socket(clientSocket)

# mail 验证
tcp_send(clientSocket, 'AUTH LOGIN', 334)

username = base64.b64encode(b'xxxxx@sina.cn').decode()
password = base64.b64encode(b'123456').decode()
tcp_send(clientSocket, username, 334)
tcp_send(clientSocket, password, 235)

# Send MAIL FROM command and print server response.
tcp_send(clientSocket, 'MAIL FROM: <xxxxx@sina.cn>', 250)
# Send RCPT TO command and print server response.
tcp_send(clientSocket, 'RCPT TO: <xxxxx@qq.com>', 250)
# Send DATA command and print server response.
tcp_send(clientSocket, 'DATA', 354)
# Send message data.
message = '''From: xxxxx@sina.cn
To: xxxxx@qq.com
Subject: tcp mail client

hello
this is mail client by python tcp.
.'''
tcp_send(clientSocket, message, 250)
# Send QUIT command and get server response.
tcp_send(clientSocket, 'QUIT', 221)
