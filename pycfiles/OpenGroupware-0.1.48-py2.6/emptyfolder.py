# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/emptyfolder.py
# Compiled at: 2012-10-12 07:02:39
from davfolder import DAVFolder
from davobject import DAVObject

class EmptyFolder(DAVFolder):
    """ Used to provide an empty read-only folder in the DAV hierarchy.

        Primarily used a place holder for objects that have not yet been
        implemented?"""

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def _load_self(self):
        """ Dummy data loader, does nothing, simply returns success."""
        return True

    def keys(self):
        """ There are no keys in an empty collection."""
        return []

    def object_for_key(self, name):
        """ Causes a 404 (Not Found) exception."""
        self.no_such_path()