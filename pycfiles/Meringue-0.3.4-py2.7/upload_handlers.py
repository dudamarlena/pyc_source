# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/upload_handlers.py
# Compiled at: 2015-08-22 16:34:49
import os.path
from hashlib import sha256
from django.core.files import uploadhandler

def _rename(v, rn):
    return ('{0}{1}').format(sha256(v).hexdigest(), os.path.splitext(rn)[1])


class MemoryFileUploadHandler(uploadhandler.MemoryFileUploadHandler):

    def file_complete(self, file_size):
        if not self.activated:
            return
        self.file_name = _rename(self.file.read(), self.file_name)
        return super(MemoryFileUploadHandler, self).file_complete(file_size)


class TemporaryFileUploadHandler(uploadhandler.TemporaryFileUploadHandler):

    def file_complete(self, file_size):
        file = super(TemporaryFileUploadHandler, self).file_complete(file_size)
        self.file_name = _rename(file.read(), self.file_name)
        return file