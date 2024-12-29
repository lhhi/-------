from socket import *  # 导入socket模块

serverSocket = socket(AF_INET, SOCK_STREAM)  # 创建TCP套接字

# 准备服务器套接字
serverSocket.bind(('localhost', 8080))  # 绑定IP地址和端口号
serverSocket.listen(1)  # 监听连接，最大连接数为1

while True:
    print('Ready to serve...')  # 打印准备服务信息
    connectionSocket, addr = serverSocket.accept()  # 接受客户端连接
    try:
        message = connectionSocket.recv(1024)  # 接收客户端请求消息
        filename = message.split()[1]  # 提取请求的文件名
        # print('filename:', filename)  # 打印请求的文件名
        f = open(filename[1:], 'rb')  # 以二进制模式打开文件
        outputdata = f.read()  # 读取文件内容
        f.close()  # 关闭文件

        # 根据文件扩展名设置Content-Type
        if filename.endswith(b'.jpg') or filename.endswith(b'.jpeg'):
            content_type = b'Content-Type: image/jpeg\r\n'
        elif filename.endswith(b'.png'):
            content_type = b'Content-Type: image/png\r\n'
        elif filename.endswith(b'.txt'):
            content_type = b'Content-Type: text/plain\r\n'
        else:
            content_type = b'Content-Type: application/octet-stream\r\n'

        # 发送HTTP响应头
        connectionSocket.send(b'HTTP/1.1 200 OK\r\n')  # 发送状态行
        connectionSocket.send(content_type)  # 发送响应头，调整内容类型
        connectionSocket.send(b'\r\n')  # 发送空行，表示头部结束

        # 将请求的文件内容发送给客户端
        connectionSocket.sendall(outputdata)  # 使用sendall确保所有数据都被发送

    except IOError:
        # 发送文件未找到的HTTP响应消息
        connectionSocket.send(b'HTTP/1.1 404 Not Found\r\n')  # 发送状态行
        connectionSocket.send(b'Content-Type: text/html\r\n')  # 发送响应头，内容类型为HTML
        connectionSocket.send(b'\r\n')  # 发送空行，表示头部结束
        connectionSocket.send(b'<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n')  # 发送响应体

    connectionSocket.close()  # 关闭连接套接字



