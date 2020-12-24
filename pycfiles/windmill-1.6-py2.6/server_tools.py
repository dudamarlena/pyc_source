# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/tools/server_tools.py
# Compiled at: 2011-01-13 01:48:00
import time, httplib, urllib, xmlrpclib, sys
if not sys.version.startswith('2.4'):
    from urlparse import urlparse
else:
    from windmill.tools.urlparse_25 import urlparse

def get_request(url, proxy_host='127.0.0.1', proxy_port=4444):
    connection = httplib.HTTPConnection(proxy_host + ':' + str(proxy_port))
    connection.request('GET', url)
    response = connection.getresponse()
    response.body = response.read()
    return response
    import xmlrpclib


class ProxiedTransport(xmlrpclib.Transport):

    def __init__(self, proxy, user_agent='python.httplib'):
        """Initialization, set the proxy location"""
        try:
            xmlrpclib.Transport.__init__(self)
        except AttributeError:
            pass

        self.proxy = proxy
        self.user_agent = user_agent

    def make_connection(self, host):
        self.realhost = host
        import httplib
        if sys.version_info[0] == 2 and sys.version_info[1] == 7 or sys.version_info[0] == 3 and sys.version_info[1] == 2:
            return httplib.HTTPConnection(self.proxy)
        else:
            return httplib.HTTP(self.proxy)

    def send_request(self, connection, handler, request_body):
        connection.putrequest('POST', 'http://%s%s' % (self.realhost, handler))

    def send_host(self, connection, host):
        connection.putheader('Host', self.realhost)