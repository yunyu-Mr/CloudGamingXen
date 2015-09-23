# -*- coding: utf-8 -*-
import os
import json
import web
import psutil

urls = (
    '/(.*)/', 'redirect',
    '/getproc', 'getproc',
    '/getserver', 'getserver'
    )
class redirect:
    def GET(self, path):
        web.seeother('/' + path)
class getproc:
    def GET(self):
        process_list = []
        for proc in psutil.process_iter():
            process_list.append(proc.name())
        return json.dumps(process_list)

class getserver(object):
    def GET(self):
        return json.dumps({'ip_addr':'0'})

application = web.application(urls, globals()).wsgifunc()
