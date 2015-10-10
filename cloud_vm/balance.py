#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import json
import web
import urllib2
import XenAPI
import datetime
import thread
import time
import ConfigParser
import operator

def test_inuse():
        db = MySQLdb.connect("172.18.216.141", "root", "netlab513", "CloudGaming")
        cursor = db.cursor()
        sql = '''SELECT server, COUNT(server) FROM CloudGaming_cluster.inuse_vms
                GROUP BY server
                ORDER BY COUNT(server);'''

        # Get configuration, available servers list:
        config = ConfigParser.ConfigParser()
        config.read("./server.conf")
        servers = dict()
        for key, server in config.items("servers"):
            servers[server] = 0
        print servers

        # Check servers using situations:
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for server, cnt in results:
                servers[server] = cnt
            print servers
            sorted_servers = sorted(servers.items(), key=operator.itemgetter(1))
            print sorted_servers
        except Exception, e:
            print e

        # Check each server
        has_vm = False
        for server_ip, cnt in sorted_servers:
            print 'Checking ', server_ip, '  cnt=', cnt
            sql = "select uuid, name, ip from CloudGaming_cluster.available_vms WHERE server=%s;" % server_ip
            ip = None
            available_vm_count = 0

            session = XenAPI.Session("http://%s" % server_ip)
            session.xenapi.login_with_password("root", "netlab")

            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                available_vm_count = len(results)
                uuid = None
                name = None
                if available_vm_count >= 1:
                    uuid = results[0][0]
                    name = results[0][1]
                    ip = results[0][2]
                    if ip == "NULL":
                        vm = session.xenapi.VM.get_by_uuid(uuid)
                        vgm = session.xenapi.VM.get_guest_metrics(vm)
                        system = session.xenapi.VM_guest_metrics.get_networks(vgm)
                        if "0/ip" in system.keys():
                            ip = system["0/ip"]
                        else:
                            raise Exception('No ip')
                else:
                    continue
                delete_sql = "delete from available_vms where uuid = '%s'" % uuid
                insert_sql = "insert into inuse_vms values('%s','%s','%s')" % (uuid, name, ip)
                cursor.execute(delete_sql)
                cursor.execute(insert_sql)
                db.commit()

                retcode = urllib2.urlopen('http://' + ip + '/rungame?id=' + id).read()
                has_vm = True
                available_vm_count = available_vm_count - 1
                print available_vm_count
            except Exception, e:
                print e

            # if available_vm_count <= 1:
            #     thread.start_new_thread(createvm, (db, session))

        if not has_vm:
            raise Exception('No available vm')




if __name__=='__main__':
    test_inuse()