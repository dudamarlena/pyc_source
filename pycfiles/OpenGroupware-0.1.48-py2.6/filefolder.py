# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/files/filefolder.py
# Compiled at: 2012-10-12 07:02:39
from coils.net import DAVFolder, DAVObject, EmptyFolder

class FilesFolder(EmptyFolder):

    def __init__(self, parent, name, **params):
        EmptyFolder.__init__(self, parent, name, **params)

    def object_for_key(self, name):
        if name in self.get_children():
            return CabinetFolder(self, name, entity=self.data[name][0], request=self.request, context=self.context)
        self.no_such_path()