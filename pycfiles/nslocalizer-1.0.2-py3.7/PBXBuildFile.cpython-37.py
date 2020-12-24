# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/xcodeproj/pbProj/PBXBuildFile.py
# Compiled at: 2019-02-23 14:43:19
# Size of source mod 2**32: 2001 bytes
from . import PBX_Constants
from .PBXItem import PBXItem

class PBXBuildFile(PBXItem):

    def __init__(self, identifier, dictionary):
        super(self.__class__, self).__init__(identifier, dictionary)

    def resolveGraph(self, project):
        super(self.__class__, self).resolveGraph(project)
        self.resolveGraphNodeForKey(PBX_Constants.kPBX_BUILDFILE_fileRef, project)