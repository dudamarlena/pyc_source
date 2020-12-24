# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pkgsync/dist.py
# Compiled at: 2013-03-02 17:41:30
import os
from hashlib import md5
import pkginfo
from .meta import Metadata, OldStyleMetadata
from .exceptions import InvalidDistribution

class Distribution(object):

    def __init__(self, path):
        self.path = path
        try:
            self.meta = Metadata(self)
        except InvalidDistribution:
            self.meta = OldStyleMetadata(self)

        self._content = None
        self._md5_digest = None
        return

    def _load(self):
        f = open(self.path, 'rb')
        self._content = f.read()
        f.close()

    def _calculate_digest(self):
        self._md5_digest = md5(self.content).hexdigest()

    @property
    def content(self):
        if not self._content:
            self._load()
        return self._content

    @property
    def basename(self):
        return os.path.basename(self.path)

    @property
    def md5_digest(self):
        if not self._md5_digest:
            self._calculate_digest()
        return self._md5_digest