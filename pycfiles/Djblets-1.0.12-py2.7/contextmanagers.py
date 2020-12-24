# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/contextmanagers.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import logging, os, signal, sys
from contextlib import contextmanager
from django.utils.translation import ugettext as _
logger = logging.getLogger(__name__)

def kill_process(pid):
    """Kill a process."""
    if sys.platform == b'win32':
        import ctypes
        PROCESS_TERMINATE = 1
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
        ctypes.windll.kernel32.TerminateProcess(handle, -1)
        ctypes.windll.kernel32.CloseHandle(handle)
    else:
        os.kill(pid, signal.SIGKILL)


@contextmanager
def controlled_subprocess(process_name, process):
    """
    A context manager for a subprocess that guarantees that a process
    is terminated, even if exceptions are thrown while using it.

    The process_name argument is used for logging when the process goes
    down fighting.  The process argument is a process returned by
    subprocess.Popen.

    Example usage:

    process = subprocess.Popen(['patch', '-o', newfile, oldfile])

    with controlled_subprocess("patch", process) as p:
        # ... do things with the process p

    Once outside the with block, you can rest assured that the subprocess
    is no longer running.
    """
    caught_exception = None
    try:
        yield process
    except Exception as e:
        caught_exception = e

    if process.returncode is None and process.poll() is None:
        logger.warning(_(b"The process '%(name)s' with PID '%(pid)s' did not exit cleanly and will be killed automatically.") % {b'name': process_name, 
           b'pid': process.pid})
        kill_process(process.pid)
        process.wait()
    if caught_exception:
        raise caught_exception
    return