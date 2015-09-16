
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set up connect
s.connect(('127.0.0.1', 9999))
# receive welcome messages
print(s.recv(1024))
# for data in ['Michael', 'Tracy', 'Sarah']:
#     # send data
#     s.send(data)
#     print(s.recv(1024))
while True:
    x = raw_input(">>")
    if x != 'exit':
        s.send(x)
        print s.recv(1024)
    else:
        break
s.send('exit')
s.close()