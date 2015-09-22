
import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set up connect
s.connect(('172.18.219.48', 9999))
# receive welcome messages
print(s.recv(1024))
# for data in ['Michael', 'Tracy', 'Sarah']:
#     # send data
#     s.send(data)
#     print(s.recv(1024))
while True:
    x = raw_input(">>")
    if x == 'login':
        req = json.dumps(
            {
                'action':'login',
                'username':'root',
                'password':'netlab'
            })
    elif x == 'start':
        req = json.dumps(
            {
                'action':'start',
                'game_name':'batman',
                'vm_type':'high'
            })
    elif x == 'what':
        req = 'what what ????'
    if x != 'exit':
        s.send(req)
        print s.recv(1024)
    else:
        break
s.send('exit')
s.close()