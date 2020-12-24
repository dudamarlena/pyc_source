# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/filestorage/blobfile/store.py
# Compiled at: 2009-09-18 09:19:43
from atreal.filestorage.blobfile.fs import BlobDir

class BlobStore(BlobDir):
    __module__ = __name__
    title = 'Blob File Store'

    def __init__(self, name, context):
        self.store_name = name
        self.context = context
        BlobDir.__init__(self, '', None)
        return