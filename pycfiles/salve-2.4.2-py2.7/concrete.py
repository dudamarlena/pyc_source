# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/filesys/concrete.py
# Compiled at: 2015-11-06 23:45:35
import os, shutil
from contextlib import contextmanager
from salve.filesys.abstract import Filesys
from salve.util import hash_from_path

class ConcreteFilesys(Filesys):

    def lookup_type(self, path):
        """
        Lookup the type of a given path.

        Args:
            @path
            The path to the file, dir, or link to lookup.
        """
        if os.path.islink(path):
            return self.element_types.LINK
        else:
            if os.path.isdir(path):
                return self.element_types.DIR
            else:
                if os.path.isfile(path):
                    return self.element_types.FILE
                return

            return

    def access(self, path, mode):
        """
        Transparent implementation of access() using os.access

        Args:
            @mode
            The type of access being inspected
        """
        return os.access(path, mode)

    def stat(self, path):
        """
        Transparent implementation of stat() using os.lstat
        """
        return os.lstat(path)

    def chmod(self, path, *args, **kwargs):
        """
        Transparent implementation of chmod() using os.chmod
        """
        return os.chmod(path, *args, **kwargs)

    def chown(self, path, uid, gid):
        """
        Transparent implementation of chown() using os.lchown
        """
        return os.lchown(path, uid, gid)

    def exists(self, path):
        """
        Transparent implementation of exists() using os.path.lexists
        """
        return os.path.lexists(path)

    def hash(self, path):
        """
        Transparent implementation of hash() using
        salve.util.hash_from_path
        """
        assert self.exists(path)
        return hash_from_path(path)

    def copy(self, src, dst):
        """
        Copies the source to the destination on the underlying filesys. Does
        not necessarily create a new entry registered to the destination.

        Args:
            @src
            The origin path to be copied. When looked up in the filesys, must
            not be None and must satisfy exists()

            @dst
            The destination path for the copy operation. The ancestors of this
            path must exist so that the file creation will not fail.
        """
        assert self.exists(src)
        src_ty = self.lookup_type(src)
        if src_ty == self.element_types.FILE:
            shutil.copyfile(src, dst)
        elif src_ty == self.element_types.DIR:
            shutil.copytree(src, dst, symlinks=True)
        elif src_ty == self.element_types.LINK:
            os.symlink(os.readlink(src), dst)
        else:
            assert False

    @contextmanager
    def open(self, path, *args, **kwargs):
        """
        Transparent implementation of open() using builtin open
        """
        with open(path, *args, **kwargs) as (f):
            yield f

    def touch(self, path, *args, **kwargs):
        """
        Touch a file by opening it in append mode and closing it
        """
        with self.open(path, 'a'):
            pass

    def symlink(self, path, target):
        """
        Transparent implementation of symlink() using os.symlink
        """
        os.symlink(path, target)

    def walk(self, path, *args, **kwargs):
        """
        Transparent implementation of walk() using os.walk
        """
        for x in os.walk(path, *args, **kwargs):
            yield x

    def mkdir(self, path, recursive=True):
        """
        Use os.mkdir or os.makedirs to create the directory desired,
        suppressing "already exists" errors.
        May still return OSError(2, 'No such file or directory') when
        nonrecursive mkdir calls have missing ancestors.
        """
        try:
            if recursive:
                os.makedirs(path)
            else:
                os.mkdir(path)
        except OSError as e:
            if e.errno == 17:
                return
            raise e

    def get_existing_ancestor(self, path):
        """
        Finds the longest prefix to a path that is known to exist.

        Args:
            @path
            An absolute path whose prefix should be inspected.
        """
        path = os.path.abspath(path)
        while not os.path.exists(path):
            path = os.path.dirname(path)

        return path