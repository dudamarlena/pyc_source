# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/minio_storage/files.py
# Compiled at: 2019-12-16 06:38:04
# Size of source mod 2**32: 4416 bytes
import tempfile, typing as T
from logging import getLogger
from django.core.files.base import File
from minio import error as merr
from minio_storage.errors import minio_error
if T.TYPE_CHECKING:
    from minio_storage.storage import Storage
logger = getLogger('minio_storage')

class ReadOnlyMixin:
    __doc__ = 'File class mixin which disallows .write() calls'

    def writable(self) -> bool:
        return False

    def write(*args, **kwargs):
        raise NotImplementedError('this is a read only file')


class NonSeekableMixin:
    __doc__ = 'File class mixin which disallows .seek() calls'

    def seekable(self) -> bool:
        return False

    def seek(self, *args, **kwargs) -> bool:
        return False


class MinioStorageFile(File):

    def __init__(self, name: str, mode: str, storage: 'Storage', **kwargs):
        self._storage = storage
        self.name = name
        self._mode = mode
        self._file = None


class ReadOnlyMinioObjectFile(MinioStorageFile, ReadOnlyMixin, NonSeekableMixin):
    __doc__ = 'A django File class which directly exposes the underlying minio object. This\nmeans the the instance doesnt support functions like .seek() and is required to\nbe closed to be able to reuse minio connections.\n\nNote: This file class is not tested yet'

    def __init__(self, name, mode, storage, max_memory_size=None, **kwargs):
        if mode.find('w') > -1:
            raise NotImplementedError('ReadOnlyMinioObjectFile storage only support read modes')
        if max_memory_size is not None:
            self.max_memory_size = max_memory_size
        super().__init__(name, mode, storage)

    def _get_file(self):
        if self._file is None:
            try:
                try:
                    obj = self._storage.client.get_object(self._storage.bucket_name, self.name)
                    self._file = obj
                    return self._file
                except merr.ResponseError as error:
                    try:
                        logger.warn(error)
                        raise OSError(f"File {self.name} does not exist")
                    finally:
                        error = None
                        del error

            finally:
                try:
                    obj.release_conn()
                except Exception as e:
                    try:
                        logger.error(str(e))
                    finally:
                        e = None
                        del e

        return self._file

    def _set_file(self, value):
        self._file = value

    file = property(_get_file, _set_file)

    def close(self):
        try:
            self.file.close()
        finally:
            self.file.release_conn()


class ReadOnlySpooledTemporaryFile(MinioStorageFile, ReadOnlyMixin):
    __doc__ = 'A django File class which buffers the minio object into a local\nSpooledTemporaryFile. '
    max_memory_size = 10485760
    max_memory_size: int

    def __init__(self, name, mode, storage, max_memory_size=None, **kwargs):
        if mode.find('w') > -1:
            raise NotImplementedError('ReadOnlySpooledTemporaryFile storage only support read modes')
        if max_memory_size is not None:
            self.max_memory_size = max_memory_size
        super().__init__(name, mode, storage)

    def _get_file(self):
        if self._file is None:
            try:
                try:
                    obj = self._storage.client.get_object(self._storage.bucket_name, self.name)
                    self._file = tempfile.SpooledTemporaryFile(max_size=(self.max_memory_size))
                    for d in obj.stream(amt=1048576):
                        self._file.write(d)

                    self._file.seek(0)
                    return self._file
                except merr.ResponseError as error:
                    try:
                        raise minio_error(f"File {self.name} does not exist", error)
                    finally:
                        error = None
                        del error

            finally:
                try:
                    obj.release_conn()
                except Exception as e:
                    try:
                        logger.error(str(e))
                    finally:
                        e = None
                        del e

        return self._file

    def _set_file(self, value):
        self._file = value

    file = property(_get_file, _set_file)

    def close(self):
        if self._file is not None:
            self._file.close()
            self._file = None