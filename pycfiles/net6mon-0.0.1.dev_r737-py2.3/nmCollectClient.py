# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/net6mon/nmCollectClient.py
# Compiled at: 2006-05-17 03:21:59
from CGIHTTPServer import CGIHTTPRequestHandler
import xmlrpclib, pmap

class nmCollectClient:
    __module__ = __name__

    def __init__(self, ip):
        self._ip = ip
        self._agent = xmlrpclib.ServerProxy('http://' + str(ip) + ':8081')

    def test_up(self):
        data = pmap.scan_host(self._ip)
        if data['hostsup'] == '1':
            return 1
        else:
            return 0

    def get_available_plugins(self):
        return self._agent.get_available_plugins()

    def get_instance_result(self, instance_name, date=0):
        if not date:
            return self._agent.get_instance_result(instance_name)
        return self._agent.get_instance_result(instance_name, date)


if __name__ == '__main__':
    collect = nmCollectClient('195.220.28.119')
    output = collect.test_up()
    print output
    output = collect.get_available_plugins()
    i = 1
    for elem in output:
        print 'Plugin ' + str(i) + ' ' + str(elem)
        i = i + 1

    print collect.get_instance_result('foo', 0)