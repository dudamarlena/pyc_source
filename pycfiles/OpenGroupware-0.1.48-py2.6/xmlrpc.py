# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/xmlrpc.py
# Compiled at: 2012-10-12 07:02:39
import xmlrpclib, time, logging
from coils.net.foundation import PathObject
from coils.core import *

class XMLRPCServer(PathObject):
    name = 'xmlrpc'

    def __init__(self, parent, bundles, **params):
        PathObject.__init__(self, parent, **params)
        self.bundles = bundles

    def do_GET(self):
        raise CoilsException('XML-RPC calls must be POST commands')

    def do_POST(self):
        result = None
        start = time.time()
        try:
            try:
                payload = self.request.get_request_payload()
                rpc = xmlrpclib.loads(payload, use_datetime=True)
                method = rpc[1].split('.')
                if len(method) < 2:
                    raise CoilsException('XML-RPC request without namespace.')
                if len(method) > 2:
                    raise CoilsException('XML-RPC with convoluted namespace.')
                namespace = method[0]
                method_name = method[1]
                parameters = rpc[0]
                for bundle in self.bundles:
                    if bundle.__namespace__ == namespace:
                        handler = bundle(self.context)
                        try:
                            call = getattr(handler, method_name)
                        except Exception, err:
                            raise CoilsException('Namespace %s has no such method as %s' % (
                             namespace, method_name))
                            break
                        else:
                            result = apply(call, parameters)
                            break
                else:
                    raise CoilsException('No such API namespace as %s' % namespace)

            except Exception, err:
                self.log.exception(err)
                if self.context.amq_available:
                    end = time.time()
                    self.context.send(None, 'coils.administrator/performance_log', {'lname': 'xmlrpc', 'oname': ('{0}.{1}').format(namespace, method_name), 
                       'runtime': end - start, 
                       'error': True})
                raise err
            else:
                if self.context.amq_available:
                    end = time.time()
                    self.context.send(None, 'coils.administrator/performance_log', {'lname': 'xmlrpc', 'oname': ('{0}.{1}').format(namespace, method_name), 
                       'runtime': end - start, 
                       'error': False})

        finally:
            self.log.debug('XML-RPC processing complete')

        if result != None:
            try:
                if self.context.user_agent_description['xmlrpc']['allowNone']:
                    result = xmlrpclib.dumps(tuple([result]), allow_none=True, methodresponse=True)
                else:
                    result = xmlrpclib.dumps(tuple([result]), methodresponse=True)
            except Exception, err:
                self.log.exception(err.message)
                raise err

        if self.context.user_agent_description['omphalos']['associativeLists']:
            associative_lists = 't'
        else:
            associative_lists = 'f'
        self.request.simple_response(200, data=result, mimetype='text/xml', headers={'X-COILS-ZOGI-PROTOCOL-LEVEL': '3A.0;-', 'X-COILS-ASSOCIATIVE-LISTS': associative_lists, 
           'X-COILS-SESSION-ID': self.context.session_id})
        return