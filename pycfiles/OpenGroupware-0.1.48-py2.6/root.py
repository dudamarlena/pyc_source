# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/sync/root.py
# Compiled at: 2012-10-12 07:02:39
import json
from coils.core import *
from coils.net import PathObject, Protocol
from container import ContactsContainer
from auth import SyncAuth

class SyncRoot(PathObject, Protocol):
    __pattern__ = 'sync'
    __namespace__ = None
    __xmlrpc__ = False

    def __init__(self, parent, **params):
        PathObject.__init__(self, parent, **params)

    def is_public(self):
        return True

    def get_name(self):
        return 'sync'

    def object_for_key(self, name):
        print self, name
        if name == 'auth':
            return SyncAuth(self, request=self.request)
        if name == 'config':
            return SyncConfg(self)
        if name == 'contacts':
            return ContactsContainer(self)