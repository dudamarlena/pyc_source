# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/keystoneredis/common/redissl.py
# Compiled at: 2013-02-13 13:57:35
import redis, ssl

class Connection(redis.Connection):

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.ca_certs = kwargs.get('ca_certs', None)
        self.cert_reqs = kwargs.get('cert_reqs', ssl.CERT_REQUIRED)
        self.keyfile = kwargs.get('keyfile', None)
        self.certfile = kwargs.get('certfile', None)
        return

    def _connect(self):
        sock = super(Connection, self)._connect()
        ssl_sock = ssl.wrap_socket(sock, keyfile=self.keyfile, certfile=self.certfile, ca_certs=self.ca_certs, cert_reqs=self.cert_reqs)
        return ssl_sock