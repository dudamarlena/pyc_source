# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/image/specs.py
# Compiled at: 2019-11-04 16:02:19
# Size of source mod 2**32: 1073 bytes
from opencontainers.struct import IntStruct
VersionMajor = 1
VersionMinor = 0
VersionPatch = 1
VersionDev = '-dev'
Version = '%d.%d.%d%s' % (VersionMajor, VersionMinor, VersionPatch, VersionDev)

class Versioned(IntStruct):

    def __init__(self, schemaVersion=None):
        super().__init__(schemaVersion or VersionMajor)