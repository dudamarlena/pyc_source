# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/lindypy/Utils.py
# Compiled at: 2011-03-07 15:10:35
"""
Some utilities to make programming with tuple spaces
easier.
"""
import signal

class TimeoutError(Exception):
    pass


class timeout(object):

    def __init__(self, seconds):
        self.seconds = seconds
        self.boom = False

    def __enter__(self):
        self.oldsig = signal.getsignal(signal.SIGALRM)
        signal.signal(signal.SIGALRM, self.bailout)
        signal.alarm(self.seconds)

    def __exit__(self, *args):
        signal.alarm(0)
        signal.signal(signal.SIGALRM, self.oldsig)
        if self.boom:
            raise TimeoutError('computation timed out')

    def bailout(self, *args):
        self.boom = True