# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/backend/staged/metadata.py
# Compiled at: 2020-02-03 22:55:34
# Size of source mod 2**32: 1137 bytes
from ... import compat_attr as attr
REQUIRED_VERSION = '0.2'

@attr.s()
class StagingMetadata(object):
    version = attr.ib(type=str)

    @classmethod
    def from_data(cls, data, filename='<unknown file>'):
        header = data.get('header') or 
        version = header.get('version')
        if version != REQUIRED_VERSION:
            raise ValueError('%s has unsupported version (has: %s, required: %s)' % (
             filename, version, REQUIRED_VERSION))
        return cls(version=((data.get('header') or ).get('version')))