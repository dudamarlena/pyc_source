# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Toolserver/XMLRPCHandler.py
# Compiled at: 2010-03-01 05:51:35
import xmlrpclib
from Toolserver.RPCHandler import rpc_handler, registerRPCHandler
from Toolserver.Config import config

class xmlrpc_handler(rpc_handler):
    _prefix = 'RPC2'
    _name = 'XMLRPC'

    def parse_request(self, data, request):
        (p, u) = xmlrpclib.getparser()
        u._encoding = config.documentEncoding
        p.feed(data)
        p.close()
        args = u.close()
        method = u.getmethodname()
        return (args, {}, [], method)

    def build_exception(self, request, excinfo, reason):
        (e, d, tb) = excinfo
        code = -32400
        if reason == 'method.unknown':
            code = -32601
        elif reason == 'method':
            code = -32500
        f = xmlrpclib.Fault(code, '%s: %s' % (e, d))
        return xmlrpclib.dumps(f, methodresponse=1, encoding=config.documentEncoding)

    def build_result(self, request, method, result):
        if result is None:
            result = ''
        return xmlrpclib.dumps((result,), methodresponse=1, encoding=config.documentEncoding)


registerRPCHandler(xmlrpc_handler)