# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/freebusy/freebusy.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.net import *
from vfbobject import VFBObject

class FreeBusy(PathObject, Protocol):
    __pattern__ = [
     'freebusy', '\\.vfb$']
    __namespace__ = None
    __xmlrpc__ = False

    def __init__(self, parent, **params):
        PathObject.__init__(self, parent, **params)

    def get_name(self):
        return 'freebusy'

    def is_public(self):
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        x = VFBObject(self, name, request=self.request, context=self.context, parameters=self.parameters)
        return x

    def do_GET(self):
        responder = VFBObject(self, self.protocol_name, request=self.request, context=self.context, parameters=self.parameters)
        responder.do_GET()

    def do_POST(self):
        raise CoilsException('POST operations not support for Free/Busy')