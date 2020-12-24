# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/portalocker.py
# Compiled at: 2013-07-04 02:24:49
"""Cross-platform (posix/nt) API for flock-style file locking.

Synopsis:

   import portalocker
   file = open("somefile", "r+")
   portalocker.lock(file, portalocker.LOCK_EX)
   file.seek(12)
   file.write("foo")
   file.close()

If you know what you're doing, you may choose to

   portalocker.unlock(file)

before closing the file, but why?

Methods:

   lock( file, flags )
   unlock( file )

Constants:

   LOCK_EX
   LOCK_SH
   LOCK_NB

Exceptions:

    LockException

Notes:

For the 'nt' platform, this module requires the Python Extensions for Windows.
Be aware that this may not work as expected on Windows 95/98/ME.

History:

I learned the win32 technique for locking files from sample code
provided by John Nielsen <nielsenjf@my-deja.com> in the documentation
that accompanies the win32 modules.

Author: Jonathan Feinberg <jdf@pobox.com>,
        Lowell Alleman <lalleman@mfps.com>,
        Rick van Hattem <Rick.van.Hattem@Fawo.nl>
Version: 0.3
URL:  https://github.com/WoLpH/portalocker
"""
__all__ = [
 'lock',
 'unlock',
 'LOCK_EX',
 'LOCK_SH',
 'LOCK_NB',
 'LockException']
import os

class LockException(Exception):
    LOCK_FAILED = 1


if os.name == 'nt':
    import win32con, win32file, pywintypes
    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    LOCK_SH = 0
    LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
    __overlapped = pywintypes.OVERLAPPED()
elif os.name == 'posix':
    import fcntl
    LOCK_EX = fcntl.LOCK_EX
    LOCK_SH = fcntl.LOCK_SH
    LOCK_NB = fcntl.LOCK_NB
else:
    raise RuntimeError('PortaLocker only defined for nt and posix platforms')
if os.name == 'nt':

    def lock(file, flags):
        hfile = win32file._get_osfhandle(file.fileno())
        try:
            win32file.LockFileEx(hfile, flags, 0, -65536, __overlapped)
        except pywintypes.error, exc_value:
            if exc_value[0] == 33:
                raise LockException(LockException.LOCK_FAILED, exc_value[2])
            else:
                raise


    def unlock(file):
        hfile = win32file._get_osfhandle(file.fileno())
        try:
            win32file.UnlockFileEx(hfile, 0, -65536, __overlapped)
        except pywintypes.error, exc_value:
            if exc_value[0] == 158:
                pass
            else:
                raise


elif os.name == 'posix':

    def lock(file, flags):
        try:
            fcntl.flock(file.fileno(), flags)
        except IOError, exc_value:
            raise LockException(*exc_value)


    def unlock(file):
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)


if __name__ == '__main__':
    from time import time, strftime, localtime
    import sys, portalocker
    log = open('log.txt', 'a+')
    portalocker.lock(log, portalocker.LOCK_EX)
    timestamp = strftime('%m/%d/%Y %H:%M:%S\n', localtime(time()))
    log.write(timestamp)
    print 'Wrote lines. Hit enter to release lock.'
    dummy = sys.stdin.readline()
    log.close()