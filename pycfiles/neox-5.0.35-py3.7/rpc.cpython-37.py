# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/rpc.py
# Compiled at: 2019-03-03 10:48:05
# Size of source mod 2**32: 1318 bytes
import logging, socket
from neox.commons.jsonrpc import ServerProxy, Fault
CONNECTION = None
_USER = None
_USERNAME = ''
_HOST = ''
_PORT = None
_DATABASE = ''
CONTEXT = {}

def server_version(host, port):
    try:
        connection = ServerProxy(host, port)
        logging.getLogger(__name__).info('common.server.version(None, None)')
        result = connection.common.server.version()
        logging.getLogger(__name__).debug(repr(result))
        return result
    except (Fault, socket.error):
        raise


def _execute(conn, *args):
    name = '.'.join(args[:3])
    args = args[3:]
    result = (getattr(conn.server, name))(*args)
    return result


def execute(conn, *args):
    return _execute(conn, *args)


class RPCProgress(object):

    def __init__(self, conn, method, args):
        self.method = method
        self.args = args
        self.conn = conn
        self.res = None
        self.error = False
        self.exception = None

    def run(self):
        try:
            res = execute(self.conn, *self.args)
        except:
            print('RPC progress... Unknown exception')

        return res


# global CONNECTION ## Warning: Unused global
# global _USER ## Warning: Unused global