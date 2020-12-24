# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/shortfuse/extra/local.py
# Compiled at: 2019-03-06 13:38:27
# Size of source mod 2**32: 4386 bytes
import logging, os
from errno import ENOENT, EIO, ENOSYS
from threading import RLock
from fuse import FuseOSError
from shortfuse.node import FileNode, DirectoryNode, FileDescriptor

class DirectoryLocal(DirectoryNode):
    pass


class CachedFileDescriptor(FileDescriptor):
    __doc__ = '\n    Implements a :py:class:`~shortfuse.node.FileDescriptor` using the local filesystem.\n    '

    def __init__(self, file_handle, *args, **kwargs):
        (FileDescriptor.__init__)(self, *args, **kwargs)
        self._lock = RLock()
        self._file_handle = file_handle

    def read(self, size, offset):
        with self._lock:
            try:
                self._file_handle.seek(offset)
                return self._file_handle.read(size)
            except:
                logging.error('Failed to read file', exc_info=1)
                raise FuseOSError(EIO)

    def write(self, data, offset):
        with self._lock:
            try:
                self._file_handle.seek(offset)
                self._file_handle.write(data)
                self.attributes.set_size(max(self.attributes.get_size(), offset + len(data)))
                return len(data)
            except:
                logging.error('Failed to write file', exc_info=1)
                raise FuseOSError(EIO)

    def truncate(self, length):
        with self._lock:
            try:
                self._file_handle.truncate(length)
                self.attributes.set_size(length)
            except:
                logging.error('Failed to truncate file', exc_info=1)
                raise FuseOSError(EIO)

    def flush(self):
        with self._lock:
            try:
                self._file_handle.flush()
            except:
                logging.error('Failed to flush file', exc_info=1)
                raise FuseOSError(EIO)

    def free(self):
        self._file_handle.close()


class CachedFileNode(FileNode):
    __doc__ = '\n    A file node backed by a local file. It is useful when the remote storage does not offer granular operations on\n    the file (ie read/write bytes at a specific offset). The file can be downloaded when calling\n    :py:meth:`FileLocal.get_path` and it can be uploaded when calling :py:meth:`FileLocal.flush`.\n\n    Args:\n        tmp_dir (str): The temporary directory in which the local file is stored.\n        parent (DirectoryNode): The parent node.\n        name (str): The basename of the file.\n        attributes (NodeAttributes): Attributes for the node\n        fs_attributes (NodeFSAttribute): The filesystem attributes for the node\n        extra_attributes (NodeExtraAttributes): Extra attributes for the node\n    '

    def __init__(self, tmp_dir, parent, name, attributes, fs_attributes, extra_attributes):
        FileNode.__init__(self, parent, name, attributes, fs_attributes, extra_attributes)
        self._tmp_dir = tmp_dir

    def has_access(self, access_mode):
        return 0

    def _get_temp_path(self):
        return os.path.join(self._tmp_dir, self.name)

    def _load_file(self):
        """
        Load the file if necessary.

        Returns:
            io.RawIOBase: A file object
        """
        with self._descriptors_lock:
            temp_path = self._get_temp_path()
            if os.path.isfile(temp_path):
                return open(temp_path, 'r+b')
            try:
                result = self._load(temp_path)
            except:
                logging.error(('Failed to load file %s to %s' % (self.path, temp_path)), exc_info=1)
                raise FuseOSError(EIO)

            self.get_attributes().set_size(os.stat(temp_path).st_size)
            return result

    def _load(self, path):
        """
        Retrieve the file content/attributes from the store backing the file system. The created file may be empty
        if it doesn't exist in the store.

        Args:
            path (str): The path at which the file should be written.

        Returns:
            io.RawIOBase: A file object

        """
        raise FuseOSError(ENOSYS)

    def _create_node_descriptor(self):
        return CachedFileDescriptor(self._load_file(), self)

    def _free_node_descriptor(self, node_descriptor):
        node_descriptor.free()
        self.attributes = node_descriptor.attributes
        self.fs_attributes = node_descriptor.fs_attributes
        self.extra_attributes = node_descriptor.extra_attributes