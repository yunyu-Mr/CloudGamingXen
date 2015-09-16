import sys, time

import XenAPI


def get_vm_info(session):
    # Find a non-template VM object
    vms = session.xenapi.VM.get_all()
    infolist = list()
    for vm in vms:
        dic = dict()
        record = session.xenapi.VM.get_record(vm)
        if record['name_label'].startswith("Cloud_Gaming"):
            dic['name_label'] = record['name_label']
            dic['power_state']= record['power_state']
            # print 'name_label:', record['name_label']
            # print 'power_state:', record['power_state']

            vgm = session.xenapi.VM.get_guest_metrics(vm)
            os = session.xenapi.VM_guest_metrics.get_networks(vgm)

            if "0/ip" in os.keys():
                dic['ip_addr'] = os["0/ip"]
                # print 'ip_addr:%s\n' % os["0/ip"]
            infolist.append(dic)
    return infolist
                
        # if not(record["is_a_template"]) and not(record["is_control_domain"]):
            # print 'UUID:',record['uuid']

def connectXen(url="http://172.18.216.179", username='root', password='netlab'):
    """
    "rtype: session
    """
    session = XenAPI.Session(url)
    session.xenapi.login_with_password(username, password)
    return session

    # for vm in vms:
    #     record = session.xenapi.VM.get_record(vm)
    #     # We cannot power-cycle templates and we should avoid touching control domains
    #     # unless we are really sure of what we are doing...
    #     if not(record["is_a_template"]) and not(record["is_control_domain"]):
    #         name = record["name_label"]
    #         print "Found VM uuid", record["uuid"], "called: ", name

    #         record = session.xenapi.VM.get_record(vm)            
    #         # Make sure the VM has powered down
    #         print "  VM '%s' is in power state '%s'" % (name, record["power_state"])
    #         if record["power_state"] == "Suspended":
    #             session.xenapi.VM.resume(vm, False, True) # start_paused = False; force = True
    #             session.xenapi.VM.clean_shutdown(vm)
    #         elif record["power_state"] == "Paused":
    #             session.xenapi.VM.unpause(vm)
    #             session.xenapi.VM.clean_shutdown(vm)
    #         elif record["power_state"] == "Running":
    #             session.xenapi.VM.clean_shutdown(vm)                
                
    #         # Power-cycle the VM a few times
    #         for i in range(1, 10):
    #             print "  beginning iteration %d" % (i)
    #             print "  ... restarting"
    #             session.xenapi.VM.start(vm, False, True) # start_paused = False; force = True
    #             print "  ... waiting 20s for the VM to boot"
    #             time.sleep(20)
    #             print "  ... suspending"
    #             session.xenapi.VM.suspend(vm)
    #             print "  ... resuming"
    #             session.xenapi.VM.resume(vm, False, True) # start_paused = False; force = True
    #             print "  ... shutting down"
    #             session.xenapi.VM.clean_shutdown(vm)

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
    session.xenapi.login_with_password(username, password)
    get_vm_info(session)