# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/posix/pidlock.py
# Compiled at: 2020-04-22 08:35:40
# Size of source mod 2**32: 2081 bytes
import os, psutil
from satella.exceptions import LockIsHeld

class PIDFileLock:
    __doc__ = "\n    Acquire a PID lock file.\n\n    Usage:\n\n    >>> with PIDFileLock('myservice.pid'):\n    >>>     ... rest of code ..\n\n    Any alternatively\n\n    >>> pid_lock = PIDFileLock('myservice.pid')\n    >>> pid_lock.acquire()\n    >>> ...\n    >>> pid_lock.release()\n\n    The constructor doesn't throw, __enter__ or acquire() does, one of:\n\n   * LockIsHeld - lock is already held. This has two attributes - pid (int), the PID of holder,\n                                  and is_alive (bool) - whether the holder is an alive process\n    "
    __slots__ = ('path', 'file_no')

    def __init__(self, pid_file, base_dir='/var/run'):
        """
        Initialize a PID lock file object

        :param pid_file: rest of path
        :param base_dir: base lock directory
        """
        self.path = os.path.join(base_dir, pid_file)
        self.file_no = None

    def release(self):
        """
        Free the lock
        """
        if self.file_no is not None:
            os.unlink(self.path)
            self.file_no = None

    def acquire(self):
        """
        Acquire the PID lock

        :raises LockIsHeld: if lock if held
        """
        try:
            self.file_no = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except (OSError, FileExistsError):
            with open(self.path, 'r') as (fin):
                data = fin.read().strip()
            try:
                pid = int(data)
            except ValueError:
                os.unlink(self.path)
                return self.acquire()

            if pid in {x.pid for x in psutil.process_iter()}:
                raise LockIsHeld(pid)
            else:
                os.unlink(self.path)
                return self.acquire()

        fd = os.fdopen(self.file_no, 'w')
        fd.write(str(os.getpid()) + '\n')
        fd.close()

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()