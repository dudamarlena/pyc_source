# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/jsonrpc.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 3892 bytes
from base64 import b64decode
import time
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer, SimpleJSONRPCRequestHandler
from . import util
from .logging import Logger

class RPCAuthCredentialsInvalid(Exception):

    def __str__(self):
        return 'Authentication failed (bad credentials)'


class RPCAuthCredentialsMissing(Exception):

    def __str__(self):
        return 'Authentication failed (missing credentials)'


class RPCAuthUnsupportedType(Exception):

    def __str__(self):
        return 'Authentication failed (only basic auth is supported)'


class VerifyingJSONRPCServer(SimpleJSONRPCServer, Logger):

    def __init__(self, *args, rpc_user, rpc_password, **kargs):
        Logger.__init__(self)
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password

        class VerifyingRequestHandler(SimpleJSONRPCRequestHandler):

            def parse_request(myself):
                if SimpleJSONRPCRequestHandler.parse_request(myself):
                    if myself.command.strip() == 'OPTIONS':
                        return True
                    try:
                        self.authenticate(myself.headers)
                        return True
                    except (RPCAuthCredentialsInvalid, RPCAuthCredentialsMissing, RPCAuthUnsupportedType) as e:
                        try:
                            myself.send_error(401, repr(e))
                        finally:
                            e = None
                            del e

                    except BaseException as e:
                        try:
                            self.logger.exception('')
                            myself.send_error(500, repr(e))
                        finally:
                            e = None
                            del e

                return False

        (SimpleJSONRPCServer.__init__)(
 self, *args, requestHandler=VerifyingRequestHandler, **kargs)

    def authenticate(self, headers):
        if self.rpc_password == '':
            return
        else:
            auth_string = headers.get('Authorization', None)
            if auth_string is None:
                raise RPCAuthCredentialsMissing()
            basic, _, encoded = auth_string.partition(' ')
            if basic != 'Basic':
                raise RPCAuthUnsupportedType()
            encoded = util.to_bytes(encoded, 'utf8')
            credentials = util.to_string(b64decode(encoded), 'utf8')
            username, _, password = credentials.partition(':')
            util.constant_time_compare(username, self.rpc_user) and util.constant_time_compare(password, self.rpc_password) or time.sleep(0.05)
            raise RPCAuthCredentialsInvalid()