import socket

ip = '127.0.0.1'
TCP_PORT = 5005

m = {"Hello, World!":"a"}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, TCP_PORT))
s.send(str(m).encode())
