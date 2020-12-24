# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/linguist/libs/file_blob.py
# Compiled at: 2013-08-31 02:31:38
from os import stat
from blob_helper import BlobHelper

class FileBlob(BlobHelper):
    """
    A FileBlob is a wrapper around a File object to make it quack
    like a Grit::Blob. It provides the basic interface: `name`,
    `data`, and `size`.
    """

    def __init__(self, path, base_path=None):
        """
        Public: Initialize a new FileBlob from a path

          path      - A path String that exists on the file system.
          base_path - Optional base to relativize the path

        Returns a FileBlob.

        """
        self.path = path
        if base_path:
            base_path = base_path.rstrip('/')
        self.name = base_path and path.replace('%s/' % base_path, '', 1) or path

    def __repr__(self):
        return '<FileBlob name:%s>' % self.name

    @property
    def stat(self):
        return stat(self.path)

    @property
    def mode(self):
        """
        Public: Read file permissions

        Returns a String like '100644'
        """
        mode = self.stat.st_mode
        return oct(mode)

    @property
    def data(self):
        """
        Public: Read file contents.

        Returns a String.
        """
        if hasattr(self, '_data'):
            return self._data
        self._data = file(self.path).read()
        return self._data

    @property
    def size(self):
        """
        Public: Get byte size

        Returns an Integer.
        """
        return self.stat.st_size