# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/cypari/Version2/build/lib.macosx-10.6-intel-2.7/cypari/version.py
# Compiled at: 2020-03-01 20:27:02
from collections import namedtuple

class Version(namedtuple('Version', ['major', 'minor', 'micro', 'tag'])):

    def __str__(self):
        return '%s.%s.%s%s' % self


version_info = Version(2, 3, 1, '')
__version__ = str(version_info)