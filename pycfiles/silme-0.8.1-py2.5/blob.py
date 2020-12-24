# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/silme/diff/blob.py
# Compiled at: 2010-06-12 17:55:55
from ..core.structure import Blob

class BlobDiff:

    def __init__(self):
        self.diff = None
        self.id = None
        self.uri = None
        return

    def empty(self):
        return not bool(self.diff)


def blobdiffto(self, blob, flags=None, values=True):
    blob_diff = BlobDiff()
    blob_diff.id = self.id
    blob_diff.uri = (self.uri, blob.uri)
    if values == True:
        if self.source == blob.source:
            blob_diff.diff = None
        else:
            blob_diff.diff = True
    return blob_diff


Blob.diff = blobdiffto