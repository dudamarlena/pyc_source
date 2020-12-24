# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/WebKit/HTTPExceptions.py
# Compiled at: 2006-10-22 17:01:00
from paste.httpexceptions import *

class HTTPAuthenticationRequired(HTTPUnauthorized):
    __module__ = __name__

    def __init__(self, realm=None, message=None, headers=None):
        headers = headers or {}
        headers['WWW-Authenticate'] = 'Basic realm=%s' % realm
        HTTPUnathorized.__init__(self, message, headers)