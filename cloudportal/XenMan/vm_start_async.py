#!/usr/bin/env python

import pprint, time, sys

import XenAPI

def vm_start_low_q(session):
    vms = session.xenapi.VM.get_all()
    for vm in vms:
        record = session.xenapi.VM.get_record(vm)
        if record['name_label'].startswith("Cloud_Gaming_Low") and record['power_state']


def vm_start(session, vmname):

    # print "Listing all VM references:"
    # vms = session.xenapi.VM.get_all()
    # pprint.pprint(vms)

    # print "Dumping all VM records:"
    # for vm in vms:
    #     pprint.pprint(session.xenapi.VM.get_record(vm))
        
    print "Attempting to start a VM called %s (if it doesn't exist this will throw an exception)" % vmname
    vm = session.xenapi.VM.get_by_name_label(vmname)[0]
    session.xenapi.VM.start(vm, False, True)

    print "Attempting to start the VM asynchronously"
    task = session.xenapi.Async.VM.start(vm, False, True)
    task_record = session.xenapi.task.get_record(task)

    print "The initial contents of the task record:"
    pprint.pprint(task_record)
    print "Waiting for the task to complete"
    while session.xenapi.task.get_status(task) == "pending": time.sleep(1)

    task_record = session.xenapi.task.get_record(task)
    print "The final contents of the task record:"
    pprint.pprint(task_record)
    
if __name__ == "__main__":
    if len(sys.argv) <> 4:
        print "Usage:"
        print sys.argv[0], " <url> <username> <password>"
        sys.exit(1)
    url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    # First acquire a valid session by logging in:
    session = XenAPI.Session(url)
    session.xenapi.login_with_password(username, password, "1.0", "xen-api-scripts-vm-start-async.py")
    # vm_start(session, 'Cloud_Gaming_VM1')
    vm_start_low_q(session)