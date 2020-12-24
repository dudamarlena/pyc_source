# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/proxy/transport.py
# Compiled at: 2012-10-12 07:02:39
import base64, xmlrpclib, httplib

class Transport(xmlrpclib.Transport):
    user_agent = 'OpenGroupware.org COILS proxy service/1.0'
    realhost = None
    proxy = None
    credentials = ()

    def set_proxy(self, proxy):
        self.proxy = proxy

    def make_connection(self, host):
        if self.proxy != None:
            self.realhost = host
            h = httplib.HTTP(self.proxy)
            return h
        else:
            return xmlrpclib.Transport.make_connection(self, host)

    def send_basic_auth(self, connection):
        auth = base64.encodestring('%s:%s' % self.credentials).strip()
        connection.putheader('Authorization', 'Basic %s' % auth)

    def send_request(self, connection, handler, request_body):
        if self.proxy != None:
            connection.putrequest('POST', 'http://%s%s' % (self.realhost, handler))
        else:
            xmlrpclib.Transport.send_request(self, connection, handler, request_body)
        return

    def send_host(self, connection, host):
        xmlrpclib.Transport.send_host(self, connection, host)
        if self.proxy != None:
            connection.putheader('Host', self.realhost)
        if self.credentials != ():
            self.send_basic_auth(connection)
        return