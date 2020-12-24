# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/portalocker.py
# Compiled at: 2013-07-04 02:24:49
__doc__ = 'Cross-platform (posix/nt) API for flock-style file locking.\n\nSynopsis:\n\n   import portalocker\n   file = open("somefile", "r+")\n   portalocker.lock(file, portalocker.LOCK_EX)\n   file.seek(12)\n   file.write("foo")\n   file.close()\n\nIf you know what you\'re doing, you may choose to\n\n   portalocker.unlock(file)\n\nbefore closing the file, but why?\n\nMethods:\n\n   lock( file, flags )\n   unlock( file )\n\nConstants:\n\n   LOCK_EX\n   LOCK_SH\n   LOCK_NB\n\nExceptions:\n\n    LockException\n\nNotes:\n\nFor the \'nt\' platform, this module requires the Python Extensions for Windows.\nBe aware that this may not work as expected on Windows 95/98/ME.\n\nHistory:\n\nI learned the win32 technique for locking files from sample code\nprovided by John Nielsen <nielsenjf@my-deja.com> in the documentation\nthat accompanies the win32 modules.\n\nAuthor: Jonathan Feinberg <jdf@pobox.com>,\n        Lowell Alleman <lalleman@mfps.com>,\n        Rick van Hattem <Rick.van.Hattem@Fawo.nl>\nVersion: 0.3\nURL:  https://github.com/WoLpH/portalocker\n'
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