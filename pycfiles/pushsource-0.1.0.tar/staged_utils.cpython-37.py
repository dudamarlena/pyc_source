# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/backend/staged/staged_utils.py
# Compiled at: 2020-02-03 23:51:01
# Size of source mod 2**32: 2467 bytes
from ... import compat_attr as attr
REQUIRED_VERSION = '0.2'

@attr.s()
class StagingFileMetadata(object):
    attributes = attr.ib(type=dict)
    filename = attr.ib(type=str)
    relative_path = attr.ib(type=str)
    sha256sum = attr.ib(type=str)


@attr.s()
class StagingMetadata(object):
    filename = attr.ib(type=str)
    file_metadata = attr.ib(type=dict)

    @classmethod
    def from_data(cls, data, filename='<unknown file>'):
        header = data.get('header') or {}
        version = header.get('version')
        if version != REQUIRED_VERSION:
            raise ValueError('%s has unsupported version (has: %s, required: %s)' % (
             filename, version, REQUIRED_VERSION))
        payload = data.get('payload') or {}
        files = payload.get('files') or []
        file_metadata = {}
        for entry in files:
            md = StagingFileMetadata(attributes=(entry.get('attributes') or {}),
              filename=(entry['filename']),
              relative_path=(entry['relative_path']),
              sha256sum=(entry['sha256sum']))
            if md.relative_path in file_metadata:
                raise ValueError('File %s listed twice in %s' % (md.relative_path, filename))
            file_metadata[md.relative_path] = md

        return cls(filename=filename, file_metadata=file_metadata)


@attr.s()
class StagingLeafDir(object):
    file_type = attr.ib(type=str)
    dest = attr.ib(type=str)
    path = attr.ib(type=str)