# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bd2k/util/lockfile.py
# Compiled at: 2018-05-03 13:55:55
from __future__ import absolute_import
import errno, logging as log, os
try:
    from lockfile.pidlockfile import PIDLockFile
except:
    pass
else:

    class SmartPIDLockFile(PIDLockFile):
        """
        A PID lock file that breaks the lock if the owning process doesn't exist
        """

        def process_alive(self, pid):
            try:
                os.kill(pid, 0)
                return True
            except OSError as e:
                if e.errno == errno.ESRCH:
                    return False
                else:
                    return

            return

        def acquire(self, timeout=None):
            owner = self.read_pid()
            if owner is not None and owner != os.getpid() and self.process_alive(owner) is False:
                log.warn("Breaking lock '%s' since owning process %i is dead." % (
                 self.lock_file, owner))
                self.break_lock()
            PIDLockFile.acquire(self, timeout)
            return