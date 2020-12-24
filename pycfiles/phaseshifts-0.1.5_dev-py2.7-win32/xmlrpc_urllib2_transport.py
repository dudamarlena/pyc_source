# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\phaseshifts\contrib\xmlrpc_urllib2_transport.py
# Compiled at: 2014-01-31 08:28:09
"""urllib2-based transport class for xmlrpclib.py (with test code).

Written from scratch but inspired by xmlrpc_urllib_transport.py file from http://starship.python.net/crew/jjkunce/ by jjk.

A. Ellerton 2006-07-06

Testing with Python 2.4 on Windows and Linux, with/without a corporate proxy in place.

****************************
*** USE AT YOUR OWN RISK ***
****************************
"""
import xmlrpclib

class ProxyTransport(xmlrpclib.Transport):
    """Provides an XMl-RPC transport routing via a http proxy.
This is done by using urllib2, which in turn uses the environment
varable http_proxy and whatever else it is built to use (e.g. the
windows registry).
NOTE: the environment variable http_proxy should be set correctly.
See checkProxySetting() below.
Written from scratch but inspired by xmlrpc_urllib_transport.py
file from http://starship.python.net/crew/jjkunce/ by jjk.
A. Ellerton 2006-07-06
"""

    def parse_response(self, file):
        return self._parse_response(file, None)

    def _parse_response(self, file, sock):
        p, u = self.getparser()
        while 1:
            if sock:
                response = sock.recv(1024)
            else:
                response = file.read(1024)
            if not response:
                break
            if self.verbose:
                print 'body:', repr(response)
            p.feed(response)

        file.close()
        p.close()
        return u.close()

    def request(self, host, handler, request_body, verbose):
        import urllib2
        self.verbose = verbose
        url = 'http://' + host + handler
        if self.verbose:
            'ProxyTransport URL: [%s]' % url
        request = urllib2.Request(url)
        request.add_data(request_body)
        request.add_header('User-Agent', self.user_agent)
        request.add_header('Content-Type', 'text/xml')
        proxy_handler = urllib2.ProxyHandler()
        opener = urllib2.build_opener(proxy_handler)
        f = opener.open(request)
        return self.parse_response(f)


def checkProxySetting():
    """If the variable 'http_proxy' is set, it will most likely be in one
of these forms (not real host/ports):
proxyhost:8080
http://proxyhost:8080
urlllib2 seems to require it to have 'http;//" at the start.
This routine does that, and returns the transport for xmlrpc.
"""
    import os, re
    try:
        http_proxy = os.environ['http_proxy']
    except KeyError:
        return

    match = re.search('(http://)?([\\w/-/.]+):([\\w/-/.]+)(\\@)?([\\w/-/.]+)?:?([\\w/-/.]+)?', http_proxy)
    if not match:
        raise Exception('Proxy format not recognised: [%s]' % http_proxy)
    else:
        groups = match.groups()
        if not groups[3]:
            os.environ['http_proxy'] = 'http://%s:%s' % (groups[1], groups(2))
        else:
            os.environ['http_proxy'] = 'http://%s:%s@%s:%s' % (groups[1], groups[2], groups[4], groups[5])


def test():
    import sys, os

    def nextArg():
        try:
            return sys.argv.pop(1)
        except:
            return

        return

    checkProxySetting()
    url = nextArg() or 'http://betty.userland.com'
    api = nextArg() or 'examples.getStateName(32)'
    try:
        server = xmlrpclib.Server(url, transport=ProxyTransport())
        print 'Url: %s' % url
        try:
            print 'Proxy: %s' % os.environ['http_proxy']
        except KeyError:
            print 'Proxy: (Apparently none)'

        print 'API: %s' % api
        r = eval('server.%s' % api)
        print 'Result: ', r
    except xmlrpclib.ProtocolError as e:
        print 'Connection error: %s' % e
    except xmlrpclib.Fault as e:
        print 'Error: %s' % e


if __name__ == '__main__':
    test()