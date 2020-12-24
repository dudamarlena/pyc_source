# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/werkzeug/posixemulation.py
# Compiled at: 2014-01-20 15:46:16
# Size of source mod 2**32: 3543 bytes
"""
    werkzeug.posixemulation
    ~~~~~~~~~~~~~~~~~~~~~~~

    Provides a POSIX emulation for some features that are relevant to
    web applications.  The main purpose is to simplify support for
    systems such as Windows NT that are not 100% POSIX compatible.

    Currently this only implements a :func:`rename` function that
    follows POSIX semantics.  Eg: if the target file already exists it
    will be replaced without asking.

    This module was introduced in 0.6.1 and is not a public interface.
    It might become one in later versions of Werkzeug.

    :copyright: (c) 2013 by the Werkzeug Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
import sys, os, errno, time, random
can_rename_open_file = False
if os.name == 'nt':
    _rename = lambda src, dst: False
    _rename_atomic = lambda src, dst: False
    try:
        import ctypes
        _MOVEFILE_REPLACE_EXISTING = 1
        _MOVEFILE_WRITE_THROUGH = 8
        _MoveFileEx = ctypes.windll.kernel32.MoveFileExW

        def _rename(src, dst):
            if not isinstance(src, unicode):
                src = unicode(src, sys.getfilesystemencoding())
            if not isinstance(dst, unicode):
                dst = unicode(dst, sys.getfilesystemencoding())
            if _rename_atomic(src, dst):
                return True
            retry = 0
            rv = False
            while not rv and retry < 100:
                rv = _MoveFileEx(src, dst, _MOVEFILE_REPLACE_EXISTING | _MOVEFILE_WRITE_THROUGH)
                if not rv:
                    time.sleep(0.001)
                    retry += 1
                    continue

            return rv


        _CreateTransaction = ctypes.windll.ktmw32.CreateTransaction
        _CommitTransaction = ctypes.windll.ktmw32.CommitTransaction
        _MoveFileTransacted = ctypes.windll.kernel32.MoveFileTransactedW
        _CloseHandle = ctypes.windll.kernel32.CloseHandle
        can_rename_open_file = True

        def _rename_atomic(src, dst):
            ta = _CreateTransaction(None, 0, 0, 0, 0, 1000, 'Werkzeug rename')
            if ta == -1:
                return False
            else:
                try:
                    retry = 0
                    rv = False
                    while not rv and retry < 100:
                        rv = _MoveFileTransacted(src, dst, None, None, _MOVEFILE_REPLACE_EXISTING | _MOVEFILE_WRITE_THROUGH, ta)
                        if rv:
                            rv = _CommitTransaction(ta)
                            break
                        else:
                            time.sleep(0.001)
                            retry += 1

                    return rv
                finally:
                    _CloseHandle(ta)

                return


    except Exception:
        pass

    def rename(src, dst):
        if _rename(src, dst):
            return
        try:
            os.rename(src, dst)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            old = '%s-%08x' % (dst, random.randint(0, sys.maxint))
            os.rename(dst, old)
            os.rename(src, dst)
            try:
                os.unlink(old)
            except Exception:
                pass


else:
    rename = os.rename
    can_rename_open_file = True