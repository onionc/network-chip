# coding:utf-8
# UDP 心跳 服务器端

from socket import socket, AF_INET, SOCK_DGRAM
import time

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12000))
print("the server is ready to receive")

lost_seconds = 10  # 心跳时间
online_list = {}  # 在线列表
while True:
    # print("waitting for client heartbeat ...")
    message, clientAddress = serverSocket.recvfrom(1024)
    print(f"message:{message}, {clientAddress}")

    if message == b'online':
        # 监测客户端
        # 返回序号和时间
        for number, ttl in online_list.copy().items():
            if ttl < time.time():
                # 删除过期的
                del online_list[number]
                continue
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ttl))
            request_message = f"{number} {time_str}"
            serverSocket.sendto(request_message.encode(), clientAddress)
        serverSocket.sendto(b"over", clientAddress)
    else:
        # 心跳客户端数据
        # 存储心跳的序号和过期时间
        sequence_number, send_time = message.decode('utf-8').split()
        online_list[sequence_number] = float(send_time)+lost_seconds
        # 返回生存时间
        send_time_s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(send_time)))
        request_message = f"ok {send_time_s} (+{lost_seconds})"
        serverSocket.sendto(request_message.encode(), clientAddress)


serverSocket.close()
