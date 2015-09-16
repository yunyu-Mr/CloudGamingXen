# server

import socket
import time, threading

from XenMan.handler import handler

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data == 'exit':
            break
        res = handler(data)
        sock.send(res)
    sock.close()
    print('Connection from %s:%s closed.' % addr)


# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind listen port
s.bind(('127.0.0.1', 9999))

s.listen(5)
print('Waiting for connection...')

while True:
    # receive a connection
    sock, addr = s.accept()
    # create new thread to handle this connection
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()

