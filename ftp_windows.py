# !/usr/bin/env/python
# !-*- coding:utf-8 -*-

import socket
import os
import sys

HOST = '192.168.78.1'
PORT = 8888

def server(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    
    # 开始监听
    s.listen(1)
    print('Listening at PORT:', port)
    conn, addr = s.accept()
    print('Connected by virtual machine:', addr)
    
    while True:
        data = conn.recv(1024).decode()
        print('received message:', data)
        # 如果TCP客户端断开连接，则本地Windows服务端也断开连接
        if not data:
            break
        command = input("Please input the command:").encode()
        conn.sendall(command)
        
    conn.close()
    s.close()

if __name__ == '__main__':
    server(HOST, PORT)
    