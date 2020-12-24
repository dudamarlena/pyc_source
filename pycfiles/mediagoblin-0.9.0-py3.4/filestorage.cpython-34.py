# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/storage/filestorage.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 4304 bytes
import io, os, shutil, six.moves.urllib.parse as urlparse
from mediagoblin.storage import StorageInterface, clean_listy_filepath, NoWebServing

class FileObjectAwareFile(io.FileIO):

    def write(self, data):
        if hasattr(data, 'read'):
            shutil.copyfileobj(data, self)
        else:
            super(FileObjectAwareFile, self).write(data)


class BasicFileStorage(StorageInterface):
    __doc__ = '\n    Basic local filesystem implementation of storage API\n    '
    local_storage = True

    def __init__(self, base_dir, base_url=None, **kwargs):
        """
        Keyword arguments:
        - base_dir: Base directory things will be served out of.  MUST
          be an absolute path.
        - base_url: URL files will be served from
        """
        self.base_dir = base_dir
        self.base_url = base_url

    def _resolve_filepath(self, filepath):
        """
        Transform the given filepath into a local filesystem filepath.
        """
        return os.path.join(self.base_dir, *clean_listy_filepath(filepath))

    def file_exists(self, filepath):
        return os.path.exists(self._resolve_filepath(filepath))

    def get_file(self, filepath, mode='r'):
        if len(filepath) > 1:
            directory = self._resolve_filepath(filepath[:-1])
            if not os.path.exists(directory):
                os.makedirs(directory)
            return FileObjectAwareFile(self._resolve_filepath(filepath), mode)

    def delete_file(self, filepath):
        """Delete file at filepath

        Raises OSError in case filepath is a directory."""
        os.remove(self._resolve_filepath(filepath))

    def delete_dir(self, dirpath, recursive=False):
        """returns True on succes, False on failure"""
        dirpath = self._resolve_filepath(dirpath)
        if recursive:
            try:
                shutil.rmtree(dirpath)
            except OSError as e:
                return False

        else:
            try:
                os.rmdir(dirpath)
            except OSError as e:
                return False

            return True

    def file_url(self, filepath):
        if not self.base_url:
            raise NoWebServing('base_url not set, cannot provide file urls')
        return urlparse.urljoin(self.base_url, '/'.join(clean_listy_filepath(filepath)))

    def get_local_path(self, filepath):
        return self._resolve_filepath(filepath)

    def copy_local_to_storage(self, filename, filepath):
        """
        Copy this file from locally to the storage system.
        """
        if len(filepath) > 1:
            directory = self._resolve_filepath(filepath[:-1])
            if not os.path.exists(directory):
                os.makedirs(directory)
            shutil.copy(filename, self.get_local_path(filepath))

    def get_file_size(self, filepath):
        return os.stat(self._resolve_filepath(filepath)).st_size