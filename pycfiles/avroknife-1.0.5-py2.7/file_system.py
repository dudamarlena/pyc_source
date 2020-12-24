# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/removing_madis_from_code/avroknife/avroknife/test/file_system.py
# Compiled at: 2015-09-04 08:27:04
import os, uuid, tempfile, shutil
from avroknife.file_system import import_hdfs_lib

class FileSystem:
    """File system abstraction"""

    def create_temporary_dir(self, dir=None):
        """
        Args:
            dir: If dir is specified, the file will be created in that directory; 
                otherwise, a default directory is used.

        Returns:
            path to the directory
        """
        raise NotImplementedError

    def delete_dir(self, path):
        raise NotImplementedError

    def create_dir(self, path):
        raise NotImplementedError

    def copy_from_local_dir(self, src_dir, dst_dir):
        """Copy directory from a local file system
        
        Args:
            dst_dir: the destination directory; it mustn't already exist.
        """
        raise NotImplementedError

    def copy_to_local_dir(self, src_dir, dst_dir):
        """Copy directory to a local file system
        
        Args:
            dst_dir: the destination directory; it mustn't already exist.
        """
        raise NotImplementedError

    def join_path(self, path_elements):
        raise NotImplementedError


class LocalFS(FileSystem):
    """Local file system"""

    def create_temporary_dir(self, dir=None):
        return tempfile.mkdtemp(dir=dir)

    def delete_dir(self, path):
        shutil.rmtree(path)

    def create_dir(self, path):
        os.makedirs(path)

    def copy_from_local_dir(self, src_dir, dst_dir):
        shutil.copytree(src_dir, dst_dir)

    def copy_to_local_dir(self, src_dir, dst_dir):
        self.copy_from_local_dir(src_dir, dst_dir)

    def join_path(self, path_elements):
        return os.path.join(*path_elements)


class HDFS(FileSystem):
    """Hadoop Distributed File System"""
    __default_tmp_dir = [
     '.tmp-avroknife']

    def __init__(self):
        hdfs, hdfspath = import_hdfs_lib()
        self.hdfs = hdfs
        self.hdfspath = hdfspath

    def create_temporary_dir(self, dir=None):
        file_exists = True
        path = None
        while file_exists:
            id_ = str(uuid.uuid4())
            if dir is not None:
                path = self.join_path([dir, id_])
            else:
                path = self.join_path(self.__default_tmp_dir + [id_])
            file_exists = self.hdfspath.exists(path)

        self.create_dir(path)
        return path

    def delete_dir(self, path):
        self.hdfs.rmr(path)

    def create_dir(self, path):
        self.hdfs.mkdir(path)

    def copy_from_local_dir(self, src_dir, dst_dir):
        self.hdfs.put(src_dir, dst_dir)

    def copy_to_local_dir(self, src_dir, dst_dir):
        self.hdfs.get(src_dir, dst_dir)

    def join_path(self, path_elements):
        return ('/').join(path_elements)