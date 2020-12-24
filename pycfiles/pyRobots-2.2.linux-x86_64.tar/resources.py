# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/robots/resources/resources.py
# Compiled at: 2015-01-26 11:58:05
from threading import Lock
import time

class Resource:

    def __init__(self, name=''):
        self.lock = Lock()
        self.name = name
        self.owner = None
        return

    def __str__(self):
        return self.name + (' (currently owned by <%s>)' % self.owner if self.owner else ' (not currently owned)')

    def __enter__(self):
        """
        Entering a 'resource' block *release* the lock, which may seem counter-intuitive.

        It is meant to used inside an action that lock the resource, to temporarly transfer the
        lock ownership to a sub-action:

        For instance:
        
        .. code-block::python

            @action
            @lock(WHEELS)
            def move(...):
                ...

            @action
            @lock(WHEELS)
            def goto(...):

                with WHEELS:
                    move(...)

        Here, ``goto()`` calls ``move()`` by first releasing the lock on
        ``WHEELS``, executing ``move()`` and reacquiring the lock, also if
        ``move()`` raises an exception.
        """
        self.release()

    def __exit__(self, exc_type, exc_value, traceback):
        self.acquire()

    def acquire(self, wait=True, acquirer='unknown'):
        if not wait:
            if self.lock.acquire(False):
                self.owner = acquirer
                return True
            else:
                return False

        else:
            while True:
                if self.lock.acquire(False):
                    self.owner = acquirer
                    return True
                time.sleep(0.1)

    def release(self):
        self.lock.release()
        self.owner = None
        return


class CompoundResource:

    def __init__(self, *args, **kwargs):
        self.resources = args
        self.name = kwargs.get('name', '')
        self.owner = None
        return

    def __str__(self):
        return self.name + (' (currently owned by <%s>)' % self.owner if self.owner else ' (not currently owned)')

    def __enter__(self):
        """ cf doc of Resource.__enter__.
        """
        self.release()

    def __exit__(self, exc_type, exc_value, traceback):
        """ cf doc of Resource.__exit__.
        """
        self.acquire()

    def acquire(self, wait=True, acquirer='unknown'):
        ok = True
        for res in self.resources:
            ok = res.acquire(wait, acquirer) and ok

        if not ok:
            return False
        self.owner = acquirer

    def release(self):
        for res in self.resources:
            res.release()

        self.owner = None
        return