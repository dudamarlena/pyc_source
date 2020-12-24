# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/skyfs/skyfsmanager.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import *

def SkyFSManager(BLOBManager):

    def __init__(self, project):
        self._project = project

    def get_path(self, document, version=None):
        raise Exception('get_path not implemented for SkyFSManager.')

    def create_path(self, document, version):
        raise Exception('create_path not implemented for SkyFSManager.')

    return