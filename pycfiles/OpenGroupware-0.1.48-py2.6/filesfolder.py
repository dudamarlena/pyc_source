# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/files/filesfolder.py
# Compiled at: 2012-10-12 07:02:39
from coils.net import DAVFolder, DAVObject, EmptyFolder
from personalfiles import PersonalFilesFolder
from teamsfolder import TeamsFolder
from addressbooks import AddressBooksFolder

class FilesFolder(DAVFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def _load_contents(self):
        self.insert_child('Personal', PersonalFilesFolder(self, 'Personal', context=self.context, request=self.request))
        self.insert_child('Teams', PersonalFilesFolder(self, 'Teams', context=self.context, request=self.request))
        self.insert_child('AddressBooks', AddressBooksFolder(self, 'AddressBooks', context=self.context, request=self.request))
        return True