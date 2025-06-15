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

### 6.8
写一个基础的 TCP 客户端确实只需要几十行代码，比如用 Python 的 `socket` 库，只要知道 IP 和端口，十几行就能收数据。
但是！实际项目中，TCP链接比log+消息队列复杂很多，这是因为：
1. 粘包/拆包
`data = recv(1024)` 不保证是一整条消息，可能一条数据被拆成两块发过来，或者几条一起发过来；
你得自己加协议解析（比如以 `\n` 结尾，或者用固定头部+长度字段）。
2. 断线重连 / 心跳检测
sigmadata 断线你要重连？自动判断“服务器没响应”？不能让你的程序“挂在那儿不动”。
3. 线程 / 异步处理
数据源是流式的，但你的主逻辑（异常分析、UI、日志记录）不能卡住；
必须用线程/asyncio/Queue来做“收数据”和“处理数据”的解耦。
4. 异常处理
recv 报错怎么办？
连接不上怎么办？
数据格式不对怎么办？
5. 真实部署环境下的 bug 难复现
比如 TCP 服务端发过来的是乱码、时间错乱、反复断连——你重启 TCP 客户端可能还连不上
✅ 解决办法就是封装一个“可靠的 TCP 输入模块”，**TCP本身不难，但写一个健壮的socket很难**

socket is a programming interface. It helps you send/receive dataflow
| 情况                    | 建议                                 |
| --------------------- | ---------------------------------- |
| sigmadata **只能用 TCP** | 就用后端跑 TCP socket 接收器，写成服务，写入数据库或内存 |
| sigmadata **能提供日志文件** | 强烈建议你选日志输入，开发简单、容错强、调试方便           |
| 你需要前端实时看到新数据          | 后端将 TCP/日志输入 → 推送前端（WebSocket最佳）   |

> “日志文件可见、可控、可回放，适合你当前这个数据不透明、迭代频繁的早期系统；TCP 是实时但高耦合，一旦挂了你甚至连日志都拿不到。”
> 对实时性要求既然不高，既然可以接受5-10分钟的延迟，那就尽量不要用TCP，稳定简单好多以太r


