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

urls = (
    '/getvm', 'getvm',
    '/exitgame', 'exitgame',
    '/newvm', 'newvm',
)

def createvm(db, session, server_ip):
    """
    :param db:
    :param session:
    :param server_ip:
    :return: status
    """
    cursor = db.cursor()
    template_vm = session.xenapi.VM.get_by_name_label('Cloud_Gaming_template')[0]
    new_vm = session.xenapi.VM.clone(template_vm, "Cloud_Gaming_" + datetime.datetime.now().strftime('%y%m%d%H%M%S%f'))
    new_vm_record = session.xenapi.VM.get_record(new_vm)
    uuid = new_vm_record['uuid']
    name = new_vm_record['name_label']
    new_ip = "NULL"
    print 'Starting new VM'
    session.xenapi.VM.start(new_vm, False, True)
    print 'Start successfully!'

    retry_count = 0
    while True:
        try:
            if retry_count > 40:
                break
            vgm = session.xenapi.VM.get_guest_metrics(new_vm)
            system = session.xenapi.VM_guest_metrics.get_networks(vgm)
            if "0/ip" in system.keys():
                new_ip = system["0/ip"]
            else:
                raise Exception('No ip')
        except XenAPI.Failure:
            retry_count += 1
            time.sleep(5)
            continue
        break
    print 'Add available VM'
    insert_sql = "insert into available_vms values('%s','%s','%s','%s')" % (uuid, name, new_ip, server_ip)
    try:
        cursor.execute(insert_sql)
        db.commit()
    except Exception, e:
        print e


class newvm:
    def GET(self):
        db = MySQLdb.connect("localhost", "root", "netlab513", "CloudGaming")
        session = XenAPI.Session("http://172.18.216.179")
        session.xenapi.login_with_password("root", "netlab")
        thread.start_new_thread(createvm, (db, session))
        return json.dumps("SUCCESS")


class getvm:
    """
    Select an available VM from a low-load server, and start GAserver on it.
    Start new VM if not enough exist.
    """
    def GET(self):
        """
        :return: VM's ip address.
        """
        input = web.input()
        id = input.id

        db = MySQLdb.connect("localhost", "root", "netlab513", "CloudGaming_cluster")
        cursor = db.cursor()

        servers = self.servers_list(db)
        # return json.dumps(servers)

        # Check each server
        has_vm = False
        ip = None
        for server_ip, cnt in servers:
            print 'Checking ', server_ip, '  cnt=', cnt
            sql = "select uuid, name, ip from available_vms WHERE server='%s';" % server_ip
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
                    # if not found available VM, continue search another server
                    continue
                delete_sql = "delete from available_vms where uuid = '%s'" % uuid
                insert_sql = "insert into inuse_vms values('%s','%s','%s','%s')" % (uuid, name, ip, server_ip)
                cursor.execute(delete_sql)
                cursor.execute(insert_sql)
                db.commit()

                retcode = urllib2.urlopen('http://' + ip + '/rungame?id=' + id).read()
                has_vm = True
                available_vm_count -= 1
            except Exception, e:
                print e

            if available_vm_count <= 1:
                print 'Start thread: Create new VM'
                thread.start_new_thread(createvm, (db, session, server_ip))

            # Once find an available VM, break
            break

        if not has_vm:
            raise Exception('No available vm')

        return json.dumps(ip)

    def servers_list(self, db):
        """
        :param db:
        :return: [[server_ip, usage_count], ]
        """
        # db = MySQLdb.connect("localhost", "root", "netlab513", "CloudGaming_cluster")
        cursor = db.cursor()
        sql = '''SELECT server, COUNT(server) FROM inuse_vms
                GROUP BY server
                ORDER BY COUNT(server);'''

        # Get configuration, available servers list:
        config = ConfigParser.ConfigParser()
        config.read("/var/www/conf/servers.conf")
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
            sorted_servers = sorted(servers.items(), key=operator.itemgetter(1))
            return sorted_servers
        except Exception, e:
            print e


class exitgame:
    """
    Kill GAServer and add the VM to available list.
    """
    def GET(self):
        """
        :return: status
        """
        input = web.input()
        ip = input.ip
        db = MySQLdb.connect("localhost", "root", "netlab513", "CloudGaming_cluster")
        cursor = db.cursor()

        url = 'http://' + ip + '/killga'
        retcode = urllib2.urlopen(url).read()
        query_sql = "select uuid, name, ip, server from inuse_vms where ip = '%s'" % ip
        try:
            cursor.execute(query_sql)
            result = cursor.fetchone()
            uuid = result[0]
            name = result[1]
            server_ip = result[3]
            delete_sql = "delete from inuse_vms where ip = '%s'" % ip
            insert_sql = "insert into available_vms values('%s','%s','%s','%s')" % (uuid, name, ip, server_ip)
            cursor.execute(delete_sql)
            cursor.execute(insert_sql)
            db.commit()
        except Exception, e:
            print e

        return json.dumps("SUCCESS")

web.config.debug = True
application = web.application(urls, globals()).wsgifunc()
