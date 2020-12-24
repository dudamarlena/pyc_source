# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/oomhandler.py
# Compiled at: 2019-11-28 13:06:28
from __future__ import absolute_import, division, print_function, unicode_literals
import logging, os, threading
from benchexec.cgroups import MEMORY
from benchexec import util
from ctypes import cdll
_libc = cdll.LoadLibrary(b'libc.so.6')
_EFD_CLOEXEC = 524288
_BYTE_FACTOR = 1000

class KillProcessOnOomThread(threading.Thread):
    """
    Thread that kills the process when they run out of memory.
    Usually the kernel would do this by itself,
    but sometimes the process still hangs because it does not even have
    enough memory left to get killed
    (the memory limit also effects some kernel-internal memory related to our process).
    So we disable the kernel-side killing,
    and instead let the kernel notify us via an event when the cgroup ran out of memory.
    Then we kill the process ourselves and increase the memory limit a little bit.

    The notification works by opening an "event file descriptor" with eventfd,
    and telling the kernel to notify us about OOMs by writing the event file
    descriptor and an file descriptor of the memory.oom_control file
    to cgroup.event_control.
    The kernel-side process killing is disabled by writing 1 to memory.oom_control.
    Sources:
    https://www.kernel.org/doc/Documentation/cgroups/memory.txt
    https://access.redhat.com/site/documentation//en-US/Red_Hat_Enterprise_Linux/6/html/Resource_Management_Guide/sec-memory.html#ex-OOM-control-notifications

    @param cgroups: The cgroups instance to monitor
    @param process: The process instance to kill
    @param callbackFn: A one-argument function that is called in case of OOM with a string for the reason as argument
    """

    def __init__(self, cgroups, pid_to_kill, callbackFn=lambda reason: None):
        super(KillProcessOnOomThread, self).__init__()
        self.name = b'KillProcessOnOomThread-' + self.name
        self._finished = threading.Event()
        self._pid_to_kill = pid_to_kill
        self._cgroups = cgroups
        self._callback = callbackFn
        cgroup = cgroups[MEMORY]
        ofd = os.open(os.path.join(cgroup, b'memory.oom_control'), os.O_WRONLY)
        try:
            self._efd = _libc.eventfd(0, _EFD_CLOEXEC)
            try:
                util.write_file((b'{} {}').format(self._efd, ofd), cgroup, b'cgroup.event_control')
                try:
                    os.write(ofd, (b'1').encode(b'ascii'))
                except OSError as e:
                    logging.debug(b'Failed to disable kernel-side OOM killer: error %s (%s)', e.errno, e.strerror)

            except EnvironmentError as e:
                os.close(self._efd)
                raise e

        finally:
            os.close(ofd)

    def run(self):
        close = os.close
        try:
            _ = os.read(self._efd, 8)
            if not self._finished.is_set():
                self._callback(b'memory')
                logging.debug(b'Killing process %s due to out-of-memory event from kernel.', self._pid_to_kill)
                util.kill_process(self._pid_to_kill)
                with open(os.path.join(self._cgroups[MEMORY], b'tasks'), b'rt') as (tasks):
                    for task in tasks:
                        util.kill_process(int(task))

                self._reset_memory_limit(b'memory.memsw.limit_in_bytes')
                self._reset_memory_limit(b'memory.limit_in_bytes')
        finally:
            close(self._efd)

    def _reset_memory_limit(self, limitFile):
        if self._cgroups.has_value(MEMORY, limitFile):
            try:
                self._cgroups.set_value(MEMORY, limitFile, str(1 * _BYTE_FACTOR * _BYTE_FACTOR * _BYTE_FACTOR * _BYTE_FACTOR * _BYTE_FACTOR))
            except IOError as e:
                logging.warning(b'Failed to increase %s after OOM: error %s (%s).', limitFile, e.errno, e.strerror)

    def cancel(self):
        self._finished.set()