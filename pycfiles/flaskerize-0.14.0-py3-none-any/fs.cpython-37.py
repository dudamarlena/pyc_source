# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/apryor/projects/flaskerize/flaskerize/fs.py
# Compiled at: 2019-08-25 06:08:12
# Size of source mod 2**32: 2521 bytes
from typing import Any, Callable, Optional
import fs
from _io import _IOBase

def default_fs_factory(path: str) -> fs.base.FS:
    from fs import open_fs
    return open_fs(path)


class StagedFileSystem:
    __doc__ = '\n    A filesystem that writes to an in-memory staging area and only commits the\n    changes when its .commit method is invoked\n    '

    def __init__(self, root: str, srcfs_factory: Callable[(..., fs.base.FS)]=default_fs_factory, dstfs_factory: Callable[(..., fs.base.FS)]=default_fs_factory):
        """
        
        Args:
            root (str): Root path of src file system
            srcfs_factory (Callable[..., FS], optional): Factory method for returning
                PyFileSystem object. Defaults to default_fs_factory.
            dstfs_factory (Callable[..., FS], optional): Factory method for returning
                PyFileSystem object. Defaults to default_fs_factory.
        """
        self.src_fs = srcfs_factory(root)
        self.dst_fs = dstfs_factory(root)
        self.stg_fs = fs.open_fs(f"mem://{root}")

    def close(self) -> None:
        pass

    def commit(self) -> None:
        """Commit the in-memory staging file system to the destination"""
        return fs.copy.copy_fs(self.stg_fs, self.dst_fs)

    def copy(self, src_path: str, dst_path: str=None) -> None:
        """Copy a file from src_path to dst_path in the staging file system"""
        return fs.copy.copy_file(self.src_fs, src_path, self.stg_fs, dst_path or src_path)

    def open(self, path: str, mode: str='r') -> _IOBase:
        """
        Open a file in the staging file system, lazily copying it from the source file
        system if the file exists on the source but not yet in memory.
        """
        if not self.stg_fs.exists(path):
            if self.src_fs.exists(path):
                self.copy(path)
        return self.stg_fs.open(path, mode=mode)


def md5(fhandle_getter):
    import hashlib
    hash_md5 = hashlib.md5()
    with fhandle_getter() as (f):
        for chunk in iter(lambda : f.read(4096), ''):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()