# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Toolserver/SOAPHandler.py
# Compiled at: 2010-03-01 05:51:16
import SOAPpy
from SOAPpy.Types import simplify
from Toolserver.Config import config
from Toolserver.RPCHandler import rpc_handler, registerRPCHandler

def characters(self, c):
    """ adds chars from a string only in system encoding """
    if self._data != None:
        self._data += c.encode(config.documentEncoding)
    return


SOAPpy.SOAPParser.characters = characters

def dump_string(self, obj, tag, typed=0, ns_map={}):
    """ delivers chars from a string only in latin-1 encoding """
    import cgi
    tag = tag or self.gentag()
    id = self.checkref(obj, tag, ns_map)
    if id == None:
        return
    else:
        try:
            data = obj._marshalData()
        except:
            data = obj

        if type(data) != type(''):
            data = data.decode(config.documentEncoding)
        self.out.append(self.dumper(None, 'string', cgi.escape(data), tag, typed, ns_map, self.genroot(ns_map), id))
        return


SOAPpy.SOAPBuilder.dump_string = dump_string
SOAPpy.SOAPBuilder.dump_str = dump_string
SOAPpy.SOAPBuilder.dump_unicode = dump_string

class soap_handler(rpc_handler):
    _prefix = 'SOAP'
    _name = 'SOAPpy'

    def simplify_value(self, value):
        return simplify(value)

    def parse_request(self, data, request):
        (r, header, body, attrs) = SOAPpy.parseSOAPRPC(data, header=1, body=1, attrs=1)
        method = r._name
        args = r._aslist()
        kw = r._asdict()
        kwnames = r._keyord
        return (args, kw, kwnames, method)

    def build_exception(self, request, excinfo, reason):
        (e, d, tb) = excinfo
        f = SOAPpy.faultType('%s:Client' % SOAPpy.NS.ENV_T, e)
        f._setDetail(str(d))
        return SOAPpy.buildSOAP(f, encoding=config.documentEncoding)

    def build_result(self, request, method, result):
        return SOAPpy.buildSOAP(kw={'%sResponse' % method: result}, encoding=config.documentEncoding)


registerRPCHandler(soap_handler)