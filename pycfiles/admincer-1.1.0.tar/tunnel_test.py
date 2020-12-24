# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_utils/net_utils/tunnel_test.py
# Compiled at: 2018-01-31 14:44:08
import urllib3, paramiko
from pprint import pprint
from httplib import HTTPConnection
import logging
logging.basicConfig(level=logging.DEBUG)

class TunnelingPoolManager(urllib3.PoolManager):

    def __init__(self, ssh_client=None, **kwargs):
        super(TunnelingPoolManager, self).__init__(**kwargs)
        self._ssh_client = ssh_client

    def _new_pool(self, scheme, host, port):
        if scheme == 'http':
            return TunnelHTTPConnectionPool(host, ssh_client=self._ssh_client, port=port)
        else:
            return super(TunnelingPoolManager, self)._new_pool(scheme, host, port)


class TunnelHTTPConnectionPool(urllib3.HTTPConnectionPool):

    def __init__(self, host, ssh_client=None, **kwargs):
        super(TunnelHTTPConnectionPool, self).__init__(host, **kwargs)
        self._ssh_client = ssh_client

    def _new_conn(self):

        def monkey_connect():
            self = conn
            print ("ch = trans.open_channel('direct-tcpip', ({0}, {1}), ('10.111.5.156', 7337))").format(self.host, self.port)
            self.sock = ssh_client.get_transport().open_channel('direct-tcpip', (self.host, self.port), ('10.111.5.156',
                                                                                                         7337))

        print ('http = HTTPconnection(host={0}, port={1})').format(self.host, self.port)
        conn = HTTPConnection(host=self.host, port=self.port)
        conn.connect = monkey_connect
        return conn


ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='10.111.5.156', username='root', password='foobar')
http = TunnelingPoolManager(ssh_client=ssh_client)
for x in range(2):
    print '\nMaking request....\n\n'
    r = http.request('GET', 'http://127.0.0.1:8080/midonet-api/routers/')
    print '\nDone with request now print output...\n\n'
    print r.status
    pprint(r.headers)
    print r.data