# Handler
import json
import XenAPI
import time, threading

from vm_info import get_vm_info, connectXen
from db import settings, table

lock_table = threading.Lock()

def start(request):
    print "start request"
    print request
    ip_addr = "172.18.216.221"
    return json.dumps({'result':0, 'ip_addr':ip_addr})

def  login(request):
    print "login request"
    session = connectXen()
    info = get_vm_info(session)
    for item in info:
        print item
    for item in info:
        print item['name_label'], item['ip_addr']
    return json.dumps({'result':0})

def exit(request):
    return 'exit'

def vmstatus(request):
    pass

def default(request):
    return 'No such command'

def handler(data):
    # args = data.split(' ')
    print data
    if (data != ''):
        try:
            request = json.loads(data)
        except Exception, e:
            raise e
        else:
            pass
        # print request
        action = request['action']
        # Get handle function name
        func = {
            'start':start,
            'login':login,
            'vmstatus':vmstatus,
            'exit':exit
        }.get(action, default) 
        # Return handler
        return func(request)
    return 'Args not enough'

def update_table():
    with lock_table:
        # modify table
        table.insert_lod(settings.lod, {"name":"saoming"})
    print table.query_lod(settings.lod)

if __name__ == '__main__':
    table.init()