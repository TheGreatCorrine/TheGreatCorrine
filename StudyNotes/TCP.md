> TCP, the Transmission Control Protocol (传输控制协议), controls the transmission of data between two devices. \
> `socket` is how your Python code actually uses that protocol to send/receive data

If sigmadata says “you can get data via TCP protocol”,
it means you must use sockets (in Python or another language) to connect, receive, and process that data.

- SigmaData: TCP Server, 它监听一个 IP 和端口，等别人来连它
- **TCP Client**: 主动连接过去，拿到它传来的数据

✅ 用 Python 建一个 TCP 客户端要做什么？
1. import socket
> `socket` 是 Python 标准库里提供的 TCP/IP 通信工具包
2. create a socket object (创建链接工具）
```bash
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```
3. 用 `connect()` 连接 sigmadata 的 IP 和port
```bash
client_socket.connect(("192.168.1.100", 18883))
```
4. 用 `recv()` 接收数据
```python
data = client_socket.recv(1024)  # 每次接收1024字节,数据通常是 bytes（二进制）格式,所以需要decode
print(data.decode('utf-8'))      # 解码后打印出来
```
5. 关闭连接（用完记得关）
```python
client_socket.close()
```

```python
import socket

# 创建 socket（用 TCP 协议）
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到 sigmadata 的服务器（IP 和端口你得问他们）
ip = "192.168.1.100"
port = 18883
client_socket.connect((ip, port))

# 循环接收数据
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    print("收到数据：", data.decode('utf-8'))

# 关闭连接
client_socket.close()
```

Bilibili server side:
```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("ip_address", port))
    s.listen()
    c, addr = s.accept()
    with c:
        print(addr, "connected")

        while True: # can only handle one connection request
            data = c.recv(1024)
            if not data:
                break
            c.sendall(data)

```

### Multithreading Socket Server
```python
def handle_client(c, adr):
    pass

while True:
    c, addr = s.aacept()

    t.threading.Thread(target=handle_client, args=(c,adr))
    t.start()
```
However, because of GIL, Python can not actually start multi threads simultaneously. Plus, it takes up extra resources.
### `selectors` - 高级I/O复用库
### `asyncio` - 异步socket代码

```bash
python -m http.server 8000
```

**IP address** is used to identify your device, while **port** is used to recognize which application that you should send your data to.
It's application to application. 点对点
There are two types of sockets: TCP and UDP.
- TCP is reliable. If you send data to another device, it will surely receive the data 可靠传输+传输效率
- 传输速度、负载情况、网络拥塞

- TCP requires the two devices to be either the client or the server. The server will be waiting to be connected
