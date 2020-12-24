# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/py/py/_process/killproc.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 648 bytes
import py, os, sys
if sys.platform == 'win32' or getattr(os, '_name', '') == 'nt':
    try:
        import ctypes
    except ImportError:

        def dokill(pid):
            py.process.cmdexec('taskkill /F /PID %d' % (pid,))


    else:

        def dokill(pid):
            PROCESS_TERMINATE = 1
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
            ctypes.windll.kernel32.TerminateProcess(handle, -1)
            ctypes.windll.kernel32.CloseHandle(handle)


else:

    def dokill(pid):
        os.kill(pid, 15)


def kill(pid):
    """ kill process by id. """
    dokill(pid)