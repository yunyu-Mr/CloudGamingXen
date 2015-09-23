# -*- coding: utf-8 -*-
import httplib
import re

def isVMRunning(host):
    conn = httplib.HTTPConnection(host)
    conn.request("GET", "/getproc")
    res = conn.getresponse()
    proc_list = res.read()
    print proc_list
    for exe in proc_list:
        if exe == "cmd.exe":
            return True
        return False

if __name__ == "__main__":
    host = "172.18.216.84"
    print isVMRunning(host)