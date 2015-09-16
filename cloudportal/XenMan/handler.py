# Handler

import XenAPI
from vm_info import get_vm_info, connectXen

def start(args):
    print "starting game %s" % args[0]
    return 'start game'

def  login(args):
    session = connectXen()
    info = get_vm_info(session)
    for item in info:
        print item
    return 'validate'

def exit(args):
    return 'exit'

def default(args):
    return 'No such command'

def handler(data):
    args = data.split(' ')
    if (len(args) >= 2):
        func = {
            'start':start,
            'login':login,
            'exit':exit
        }.get(args[0], default) 
        return func(args[1:])
    return 'Args not enough'