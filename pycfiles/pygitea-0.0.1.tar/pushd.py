# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/gitdata/pushd.py
# Compiled at: 2019-03-15 07:56:09
__doc__ = '\nThis file contains the definition of a class that can be used like shell\npushd and popd.\n\nThe Dir object is a context_manager that can be used with the Python \'with\'\nclause.  The context manager idiom allows the user to execute some commands\nin a working directory other than the CWD and return without needing to\nexplicitly handle it.\n\nExample:\n\n  # os.getcwd() returns /tmp/somewhere\n  with Dir("/tmp/somewhere/else"):\n      # os.getcwd() returns /tmp/somewhere/else\n      ....\n\n  # os.getcwd() returns /tmp/somewhere\n'
import os, threading

class Dir(object):
    """
    Context manager to handle directory changes safely.

    On `__enter__`, `chdir`s to the given directory and on `__exit__`, `chdir`s
    back to restore the previous `cwd`.

    The current directory is also kept on thread-local storage and can be
    accessed (e.g. by multi-threaded programs that cannot rely on `chdir`) via
    the `getcwd` static method.
    """
    _tl = threading.local()

    def __init__(self, newdir):
        self.dir = newdir
        self.previous_dir = None
        return

    def __enter__(self):
        self.previous_dir = self.getcwd()
        os.chdir(self.dir)
        self._tl.cwd = self.dir
        return self.dir

    def __exit__(self, *args):
        os.chdir(self.previous_dir)
        self._tl.cwd = self.previous_dir

    @classmethod
    def getcwd(cls):
        """
        Provide a context dependent current working directory. This method
        will return the directory currently holding the lock.
        """
        if not hasattr(cls._tl, 'cwd'):
            cls._tl.cwd = os.getcwd()
        return cls._tl.cwd