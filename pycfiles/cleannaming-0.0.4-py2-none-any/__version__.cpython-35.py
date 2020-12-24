# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/cosmin/workspace/github/cleanmymac/build/lib/cleanmymac/__version__.py
# Compiled at: 2016-03-06 17:09:35
# Size of source mod 2**32: 814 bytes
from collections import namedtuple
__author__ = 'basca'
VersionSpec = namedtuple('VersionSpec', ['major', 'minor', 'revision'])
version = VersionSpec(0, 1, 16)
str_version = '.'.join(map(str, version))