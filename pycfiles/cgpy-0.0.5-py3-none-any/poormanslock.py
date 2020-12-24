# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\utils\poormanslock.py
# Compiled at: 2012-02-03 05:34:20
__doc__ = '\nPoor man\'s file locking: Create exclusively-locked dummy file, delete when done.\n\nStatements inside a "with Lock():" block are executed while other tasks pause.\nThe constructor, Lock(lockname="lock", retry_delay=0.1, max_wait=30)\ncreates a dummy file (called "lock" by default), but only if it does not \nalready exist. If the file already exists, the constructor will wait \n"retry_delay" seconds before retrying. Waiting too long ("max_wait") triggers \nan IOError exception.\n\n\nTypical usage:\n\nfrom poormanslock import Lock\n\nwith Lock():\n    pass # <insert something to do while other tasks wait>\n\nwith Lock(lockname="locked.txt", retry_delay=0.2, max_wait=10):\n    pass # <insert something to do here>\n\n\nTo turn on debug-level logging:\n\n>>> import poormanslock, logging\n>>> poormanslock.log.setLevel(logging.DEBUG)                    # doctest: +SKIP\n'
import os, time, signal, logging
from random import random
log = logging.getLogger('poormanslock')
log.addHandler(logging.StreamHandler())
fmtstr = '%(' + (')s\t%(').join(('asctime levelname name lineno process message').split()) + ')s'
log.handlers[0].setFormatter(logging.Formatter(fmtstr))
hasalarm = hasattr(signal, 'alarm')
if not hasalarm:
    import warnings
    warnings.warn("signal.alarm() not available, timeout won't work")

def _timeout(signum, frame):
    """Signal handler for Lock timeout"""
    message = 'Timed out waiting to acquire lock'
    log.error(message)
    raise IOError(message)


class Lock(object):
    """
    Poor man's file locking: Create exclusively-locked dummy file, delete when done.
    
    Statements inside a "with Lock():" block are executed while other tasks pause.
    The constructor, Lock(lockname="lock", retry_delay=0.1, max_wait=30)
    creates a dummy file (called "lock" by default), but only if it does not 
    already exist. If the file already exists, the constructor will wait 
    "retry_delay" seconds before retrying. Waiting too long ("max_wait") triggers 
    an IOError exception.
    """

    def __init__(self, lockname='lock', retry_delay=0.1, max_wait=30):
        """
        Create file "lockname" if not exists, retry until timeout if needed.
        """
        self.lockname = lockname
        self.retry_delay = retry_delay
        self.max_wait = max_wait
        self.fd = None
        if hasalarm:
            signal.signal(signal.SIGALRM, _timeout)
        return

    def __enter__(self):
        """Enter context of with statement"""
        if hasalarm:
            signal.alarm(self.max_wait)
        while self.fd is None:
            try:
                log.debug('Requesting lock')
                self.fd = os.open(self.lockname, os.O_EXCL | os.O_CREAT)
                log.debug('Acquired lock')
            except OSError:
                log.debug('Failed to acquire lock')
                time.sleep((0.5 + 0.5 * random()) * self.retry_delay)

        if hasalarm:
            signal.alarm(0)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context of with statement, closing and removing lockfile"""
        os.close(self.fd)
        os.remove(self.lockname)
        log.debug('Released lock')
        return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()