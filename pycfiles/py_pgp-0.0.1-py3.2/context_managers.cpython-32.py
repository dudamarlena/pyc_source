# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/context_managers.py
# Compiled at: 2015-08-31 08:17:33


class LockingContextManager(object):

    def __init__(self, lockable, passphrase):
        self.lockable = lockable
        self.passphrase = passphrase

    def __enter__(self):
        self.lockable.unlock(self.passphrase)
        return self.lockable

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lockable.lock()
        return False


def unlocked(lockable, passphrase):
    return LockingContextManager(lockable, passphrase)