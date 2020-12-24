# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uthreads/timer.py
# Compiled at: 2009-03-01 16:01:30
from __future__ import absolute_import
import os, sys, time, types
from twisted.internet import defer, reactor
from .core import uThread, spawn
__all__ = [
 'Timer']

class Timer(object):
    """
    Schedule a microthreaded function to be called at some future time,
    in a new microthread.  Timers can be cancelled at any time before they
    have fired.

    @ivar delayedcall: a delayed call object, if running; otherwise None
    @type delayedcall: L{twisted.internet.interfaces.IDelayedCall}

    @ivar generator: the generator supplied to the set function
    """
    __slots__ = [
     'delayedcall', 'generator']

    def __init__(self):
        self.delayedcall = None
        return

    def set(self, delay, generator):
        uThread._generator_seen(generator)
        if type(generator) is not types.GeneratorType:
            raise RuntimeError('%r is not a generator (perhaps you used a regular function?)' % (generator,))
        if self.delayedcall:
            self.clear()
        self.generator = generator
        self.delayedcall = reactor.callLater(delay, self.fire)

    def fire(self):
        spawn(self.generator)
        self.delayedcall = None
        return

    def clear(self):
        if not self.delayedcall:
            return
        self.delayedcall.cancel()
        self.delayedcall = None
        return