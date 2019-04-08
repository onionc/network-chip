# coding:utf-8
# ping程序 客户端

from socket import socket, AF_INET, SOCK_DGRAM
import time

# 配置
host, port = '192.168.10.211', 12000
times = 10  # 次数
timeout = 1  # 超时时间

# 创建Socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# 设置超时时间为1s
clientSocket.settimeout(timeout)

print(f"\n正在Ping {host}:{port} 具有 32 字节的数据：(为什么有端口，因为俺是UDP啊)")

success_ms = []  # 成功接收用时，用于统计
for i in range(1, times+1):
    message = "abcdefghijklmnopqrstuvwabcdefghi"
    clientSocket.sendto(message.encode('utf-8'), (host, port))
    try:
        # 计算时间，由于上面设置timeout，超过会抛time out
        start_ms = int(time.time()*1000)
        rep_message, serverAddress = clientSocket.recvfrom(2048)
        end_ms = int(time.time()*1000)
        gap = end_ms-start_ms
        print(f"{i} 来自 {host} 的回复：字节=32 时间={gap}ms TTL=?")
        success_ms.append(gap)
    except Exception as e:
        print(f"{i} 请求超时。({e})")
        continue

# 输出统计信息
print(f"\n{host} 的 Ping 统计信息：")
success_times = len(success_ms)
failed_times = times-success_times
lost_scale = failed_times*100//times
print(f"\t数据包：已发送 = {times}，已接收 = {success_times}，\
丢失 = {failed_times} （{lost_scale}% 丢失）")

if success_times > 0:
    # 往返行程估计时间
    print("往返行程的估计时间（以毫秒为单位）：")
    print(f"\t最短 = {min(success_ms)}ms，最长 = {max(success_ms)}ms，\
平均 = {sum(success_ms)//success_times}ms")

# 关闭Socket
clientSocket.close()