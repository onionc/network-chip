# coding:utf-8
# web代理服务器 单线程、仅支持HTTP

import socket
import sys
import re
from hashlib import md5
import os


def hash_req(s):
    """ 将请求哈希为文件名 """
    # 缓存存储目录路径
    cache_dir = r'./cache'
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    if not isinstance(s, bytes):
        s = s.encode()
    m = md5()
    m.update(s)
    filename = m.hexdigest()+'.prx'
    return os.path.join(cache_dir, filename)


# 验证参数，初始化代理IP和端口
if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n '
          'server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

if sys.argv[1] == 'd':
    ip = ''
else:
    ip = sys.argv[1]
port = 1081

# 创建socket，绑定端口并开始监听
tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.bind((ip, port))
tcpSerSock.listen(1)
print(f"proxy server: {ip}:{port}")
while 1:
    # Strat receiving data from the client
    # print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    # print('Received a connection from:', addr)

    # 获取源请求
    message = tcpCliSock.recv(1024)
    print("源请求：", message)
    if not message:
        continue
    #message = message.decode('utf-8')

    # 获取请求的属性
    http_method = message.split()[0]
    req_path = message.split()[1]
    path_data = re.findall(b'((https?):\/\/([^/]+))?(\/.+)?', req_path)

    if path_data[0] and http_method in [b'GET', b'POST']:
        # path_data[0] = [s.decode() for s in path_data[0]]
        _, r_protocal, r_host, r_url = [s.decode() for s in path_data[0]]
        print(http_method, r_protocal, r_host, r_url)
    else:
        tcpCliSock.send(b"HTTP/1.1 501 Invalid request.\n\n")
        tcpCliSock.close()
        continue

    cache_file = hash_req(req_path)
    fileExist = False
    try:
        # 代理服务器找到缓存文件并响应
        with open(cache_file, "r", encoding='utf-8') as f:
            for line in f.readlines():
                fileExist = True
                tcpCliSock.send(line.encode('utf-8'))

        if not fileExist:
            raise IOError('empty')

        print('Read from cache')

        # 未找到缓存文件的异常处理
    except (IOError, FileNotFoundError) as e:
        if fileExist is False:
            # 代理服务器创建socket
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 设置超时
            c.settimeout(10)

            print('host:', r_host)
            try:
                # 连接socket到目的主机80端口
                c.connect((r_host, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('wrb', encoding='utf-8')

                # cookie设置
                r_cookie = re.findall(b'Cookie: ([^\r\n]*)', message)
                r_cookie = r_cookie[0].decode() if r_cookie else ''

                # 发送请求
                if http_method == b'GET':
                    request = f"""\
GET http://{r_host}{r_url} HTTP/1.0
Host: {r_host}
Cookie: {r_cookie}

"""
                elif http_method == b'POST':
                    # 获取post参数
                    r_post_data = re.findall(b'\r\n\r\n((.|\n)*)', message)[0][0]
                    r_content_type = re.findall(b'Content-Type: ([^\r\n]*)', message)[0]

                    request = f"""\
POST http://{r_host}{r_url} HTTP/1.0
Host: {r_host}
Content-Type: {r_content_type.decode()}
Content-Length: {len(r_post_data)}
Cookie: {r_cookie}

{r_post_data.decode()}"""

                print("代理请求", request.encode())
                # c.send(request.encode())
                fileobj.write(request.encode())
                fileobj.flush()

                # 接收响应
                response_data = b''
                # response_data = c.recv(1024)
                for line in fileobj.readlines():
                    response_data += line
                print("响应", response_data)

                # 响应200 + GET请求 时，再做存储
                resp_code = re.findall(b"^HTTP[^ ]+ +(\d+)", response_data)[0]
                if int(resp_code) == 200 and http_method == b'GET':
                    with open(cache_file, 'wb') as f:
                        f.write(response_data)

                tcpCliSock.sendall(response_data)

            except socket.timeout as e:
                response = """\
HTTP/1.1 504 Gateway Time-out
Content-Type: text/plain; charset=utf-8
Connection: close

Failed: 超时，实在是获取不到!
"""
                tcpCliSock.sendall(response.encode('utf-8'))

            except (socket.gaierror, Exception) as e:

                print("Failed: 非法请求", e)
                response = """\
HTTP/1.1 501 Not Implemented
Content-Type: text/plain; charset=utf-8
Connection: close

Failed: 非法请求
"""
                tcpCliSock.sendall(response.encode('utf-8'))

            tcpCliSock.close()

        else:
            # HTTP response message for file not found
            print("not found")
            # Close the client and the server sockets
            tcpCliSock.close()

tcpSerSock.close()
