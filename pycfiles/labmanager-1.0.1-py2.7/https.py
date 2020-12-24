# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/suds/transport/https.py
# Compiled at: 2014-02-26 03:37:27
"""
Contains classes for basic HTTP (authenticated) transport implementations.
"""
import urllib2 as u2
from logging import getLogger
from suds.transport.http import HttpTransport
log = getLogger(__name__)

class HttpAuthenticated(HttpTransport):
    """
    Provides basic http authentication that follows the RFC-2617 specification.
    As defined by specifications, credentials are provided to the server
    upon request (HTTP/1.0 401 Authorization Required) by the server only.
    @ivar pm: The password manager.
    @ivar handler: The authentication handler.
    """

    def __init__(self, **kwargs):
        """
        @param kwargs: Keyword arguments.
            - B{proxy} - An http proxy to be specified on requests.
                 The proxy is defined as {protocol:proxy,}
                    - type: I{dict}
                    - default: {}
            - B{timeout} - Set the url open timeout (seconds).
                    - type: I{float}
                    - default: 90
            - B{username} - The username used for http authentication.
                    - type: I{str}
                    - default: None
            - B{password} - The password used for http authentication.
                    - type: I{str}
                    - default: None
        """
        HttpTransport.__init__(self, **kwargs)
        self.pm = u2.HTTPPasswordMgrWithDefaultRealm()

    def open(self, request):
        self.addcredentials(request)
        return HttpTransport.open(self, request)

    def send(self, request):
        self.addcredentials(request)
        return HttpTransport.send(self, request)

    def addcredentials(self, request):
        credentials = self.credentials()
        if None not in credentials:
            u = credentials[0]
            p = credentials[1]
            self.pm.add_password(None, request.url, u, p)
        return

    def credentials(self):
        return (
         self.options.username, self.options.password)

    def u2handlers(self):
        handlers = HttpTransport.u2handlers(self)
        handlers.append(u2.HTTPBasicAuthHandler(self.pm))
        return handlers


class WindowsHttpAuthenticated(HttpAuthenticated):
    """
    Provides Windows (NTLM) http authentication.
    @ivar pm: The password manager.
    @ivar handler: The authentication handler.
    @author: Christopher Bess
    """

    def u2handlers(self):
        try:
            from ntlm import HTTPNtlmAuthHandler
        except ImportError:
            raise Exception('Cannot import python-ntlm module')

        handlers = HttpTransport.u2handlers(self)
        handlers.append(HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(self.pm))
        return handlers