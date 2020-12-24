# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/files/move.py
# Compiled at: 2018-07-11 18:15:30
"""
Move a file in the safest way possible::

    >>> from django.core.files.move import file_move_safe
    >>> file_move_safe("/tmp/old_file", "/tmp/new_file")
"""
import os
from django.core.files import locks
try:
    from shutil import copystat
except ImportError:
    import stat

    def copystat(src, dst):
        """Copy all stat info (mode bits, atime and mtime) from src to dst"""
        st = os.stat(src)
        mode = stat.S_IMODE(st.st_mode)
        if hasattr(os, 'utime'):
            os.utime(dst, (st.st_atime, st.st_mtime))
        if hasattr(os, 'chmod'):
            os.chmod(dst, mode)


__all__ = [
 'file_move_safe']

def _samefile(src, dst):
    if hasattr(os.path, 'samefile'):
        try:
            return os.path.samefile(src, dst)
        except OSError:
            return False

    return os.path.normcase(os.path.abspath(src)) == os.path.normcase(os.path.abspath(dst))


def file_move_safe(old_file_name, new_file_name, chunk_size=65536, allow_overwrite=False):
    """
    Moves a file from one location to another in the safest way possible.

    First, tries ``os.rename``, which is simple but will break across filesystems.
    If that fails, streams manually from one file to another in pure Python.

    If the destination file exists and ``allow_overwrite`` is ``False``, this
    function will throw an ``IOError``.
    """
    if _samefile(old_file_name, new_file_name):
        return
    else:
        try:
            os.rename(old_file_name, new_file_name)
            return
        except OSError:
            pass

        with open(old_file_name, 'rb') as (old_file):
            fd = os.open(new_file_name, os.O_WRONLY | os.O_CREAT | getattr(os, 'O_BINARY', 0) | (not allow_overwrite and os.O_EXCL or 0))
            try:
                locks.lock(fd, locks.LOCK_EX)
                current_chunk = None
                while current_chunk != '':
                    current_chunk = old_file.read(chunk_size)
                    os.write(fd, current_chunk)

            finally:
                locks.unlock(fd)
                os.close(fd)

        copystat(old_file_name, new_file_name)
        try:
            os.remove(old_file_name)
        except OSError as e:
            if getattr(e, 'winerror', 0) != 32 and getattr(e, 'errno', 0) != 13:
                raise

        return