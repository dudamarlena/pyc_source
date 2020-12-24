# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/sync/container.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.net import PathObject
from sync import SyncSync
from items import SyncItems
from keys import SyncKeys

class SyncContainer(PathObject):

    def __init__(self, parent, **params):
        PathObject.__init__(self, parent, **params)

    def authenticate(self):
        pass

    def object_for_key(self, name):
        if self.authenticate():
            if name == 'sync':
                return SyncSync(self)
            if name == 'keys':
                return SyncKeys(self)
            if name == 'items':
                return SyncItems(self)


class ContactsContainer(SyncContainer):

    def __init__(self, parent, **params):
        SyncContainer.__init__(self, parent, **params)

    def load_contacts(self):
        pass