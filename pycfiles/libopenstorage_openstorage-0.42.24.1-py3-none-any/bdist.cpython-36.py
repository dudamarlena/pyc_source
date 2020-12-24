# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pkginfo/pkginfo/bdist.py
# Compiled at: 2020-01-10 16:25:33
# Size of source mod 2**32: 1198 bytes
import os, zipfile
from .distribution import Distribution

class BDist(Distribution):

    def __init__(self, filename, metadata_version=None):
        self.filename = filename
        self.metadata_version = metadata_version
        self.extractMetadata()

    def read(self):
        fqn = os.path.abspath(os.path.normpath(self.filename))
        if not os.path.exists(fqn):
            raise ValueError('No such file: %s' % fqn)
        else:
            if fqn.endswith('.egg'):
                archive = zipfile.ZipFile(fqn)
                names = archive.namelist()

                def read_file(name):
                    return archive.read(name)

            else:
                raise ValueError('Not a known archive format: %s' % fqn)
        try:
            tuples = [x.split('/') for x in names if 'PKG-INFO' in x]
            schwarz = sorted([(len(x), x) for x in tuples])
            for path in [x[1] for x in schwarz]:
                candidate = '/'.join(path)
                data = read_file(candidate)
                if b'Metadata-Version' in data:
                    return data

        finally:
            archive.close()

        raise ValueError('No PKG-INFO in archive: %s' % fqn)