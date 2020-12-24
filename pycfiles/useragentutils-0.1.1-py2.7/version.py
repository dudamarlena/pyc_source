# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/useragentutils/version.py
# Compiled at: 2013-01-04 18:25:17
import utilities as util

class Version(util.Base):
    __metaclass__ = type

    def __init__(self, version, majorVersion, minorVersion):
        self.version = version
        self.majorVersion = majorVersion
        self.minorVersion = minorVersion

    def __str__(self):
        return self.version

    def __repr__(self):
        return '<' + type(self).__name__ + ':' + self.majorVersion + '.' + self.minorVersion + '>'