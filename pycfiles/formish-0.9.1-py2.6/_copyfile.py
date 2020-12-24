# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/formish/_copyfile.py
# Compiled at: 2010-01-04 05:35:21
__all__ = [
 'copyfileobj']
import shutil
try:
    from fadvise import posix_fadvise, POSIX_FADV_DONTNEED

    def copyfileobj(fsrc, fdst, length=16384, advise_after=1048576):
        """
        Reimplementation of shutil.copyfileobj that advises the OS to remove
        parts of the source file from the OS's caches once copied to the
        destination file.

        Usage profile:
            * You have a (potentially) large file to copy.
            * You know you don't need to access the source file once copied.
            * You're quite likely to access the destination file soon after.
        """
        if not hasattr(fsrc, 'fileno'):
            return shutil.copyfileobj(fsrc, fdst, length)
        advise_after_blocks = int(advise_after / length)
        blocks_read = 0
        while True:
            data = fsrc.read(length)
            if not data:
                break
            fdst.write(data)
            blocks_read += 1
            if not blocks_read % advise_after_blocks:
                posix_fadvise(fsrc.fileno(), 0, length * blocks_read, POSIX_FADV_DONTNEED)

        posix_fadvise(fsrc.fileno(), 0, 0, POSIX_FADV_DONTNEED)


except ImportError:
    copyfileobj = shutil.copyfileobj