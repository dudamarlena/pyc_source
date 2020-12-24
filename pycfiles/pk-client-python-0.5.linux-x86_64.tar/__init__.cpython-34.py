# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anrosent/src/python/pk/pk-client-python/.venv/lib/python3.4/site-packages/pk_client/__init__.py
# Compiled at: 2015-11-21 23:01:46
# Size of source mod 2**32: 1428 bytes
import logging, json
from collections import namedtuple
import pk_common as common
logger = logging.getLogger(__name__)

class PkClient:

    def __init__(self, host, secret):
        self.host = host
        self.secret = secret
        self.knocks = common._make_knocks(secret)
        self.localaddr = ('localhost', None)

    def connect(self):
        for ix, k in enumerate(self.knocks):
            sock = self._connect_single(k)
            if ix == len(self.knocks) - 1:
                logger.debug('Success! Receiving hidden service port')
                data = sock.recv(1024).decode('utf8')
                service_port = json.loads(data)['port']
                logger.info('Hidden service port is %s' % service_port)
            sock.close()

        return self._connect_single(service_port)

    def _connect_single(self, k):
        _, lport = self.localaddr
        logger.debug('Knocking (%s,%s)' % (self.host, k))
        if not lport:
            logger.debug('No client socket bound')
            sock = common.sock_open(self.host, k)
            logger.debug('Binding to %s' % str(sock.getsockname()))
            self.localaddr = sock.getsockname()
        else:
            sock = common.sock_open(self.host, k, localaddr=self.localaddr)
        return sock

    def get_knocks(self):
        return self.knocks

    def close(self):
        pass