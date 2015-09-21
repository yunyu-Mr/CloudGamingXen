# Portal Server
#
# It's a portal of cloud gaming.
# Cliet first visit portal server to obtain gaming server's address, 
# then connect gaming server.
#
# In addition, portal server is a schedulor of gaming VMs.
# It'll start up VMs when VMs are not enough and shutdown some when they are too many.
#
# Author: Saoming
# 

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
        print 'respond:', res

        sock.send(res)
    sock.close()
    print('Connection from %s:%s closed.' % addr)


# Constants define
IP_ADDR = "172.18.219.135"
PORT = 9999
MAX_LISTEN_NUM = 5

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind listen port
s.bind((IP_ADDR, PORT))

s.listen(MAX_LISTEN_NUM)
print('Waiting for connection...')

while True:
    # receive a connection
    sock, addr = s.accept()
    # create new thread to handle this connection
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()