# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/sync/auth.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.net import PathObject

class SyncLogin(PathObject):

    def __init__(self, parent, **params):
        PathObject.__init__(self, parent, **params)

    def is_public(self):
        return True

    def get_name(self):
        return 'login'

    def do_POST(self):
        print self.get_path()
        payload = self.request.get_request_payload()
        print payload
        import pprint
        pprint.pprint(self)
        response = 'Yo'
        self.request.send_response(200, 'OK')
        self.request.send_header('Content-Length', str(len(response)))
        self.request.send_header('Content-Type', 'text/plain')
        self.request.end_headers()
        self.request.wfile.write(response)
        self.request.wfile.flush()


class SyncLogout(PathObject):

    def __init__(self, parent, **params):
        PathObject.__init__(self, parent, **params)


class SyncAuth(PathObject):

    def __init__(self, parent, **params):
        PathObject.__init__(self, parent, **params)

    def is_public(self):
        return True

    def get_name(self):
        return 'auth'

    def object_for_key(self, name):
        print self, name
        if name == 'login':
            return SyncLogin(self, request=self.request)
        if name == 'logout':
            return SyncLogout(self)