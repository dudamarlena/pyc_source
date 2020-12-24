# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparked/events.py
# Compiled at: 2011-01-09 06:01:51
"""
Classes which define a generic event system.
"""
from twisted.python import log
from twisted.words.xish import utility

class EventDispatcher(utility.EventDispatcher):
    """
    The sparked event dispatcher is simpler than the twisted version:
    it does not use XPath arguments and its event prefix is always
    empty.

    This class exists to simplify the implementation of event
    dispatchers in sparked without the syntactic sugar of xish'
    EventDispatcher class.

    It adds an extra feature: the possibility to give a parent
    dispatcher using C{setEventParent} to which events will be
    dispatched as well.
    """
    parent = None
    verbose = False

    def __init__(self, eventprefix=''):
        utility.EventDispatcher.__init__(self, eventprefix)

    def dispatch(self, event, *arg, **kwarg):
        """
        Dispatch the named event to all the callbacks.
        """
        foundTarget = False
        if self.verbose:
            log.msg('%s --> %s: %s %s' % (repr(self), event, arg, kwarg))
        self._dispatchDepth += 1
        observers = self._eventObservers
        priorities = observers.keys()
        priorities.sort()
        priorities.reverse()
        emptyLists = []
        for priority in priorities:
            for (query, callbacklist) in observers[priority].iteritems():
                if query == event:
                    callbacklist.callback(*arg, **kwarg)
                    foundTarget = True
                    if callbacklist.isEmpty():
                        emptyLists.append((priority, query))

        for (priority, query) in emptyLists:
            del observers[priority][query]

        self._dispatchDepth -= 1
        if self._dispatchDepth == 0:
            for f in self._updateQueue:
                f()

            self._updateQueue = []
        if self.parent:
            self.parent.dispatch(event, *arg, **kwarg)
        return foundTarget

    def setEventParent(self, p):
        """
        Set a parent to which events will be dispatched as well.
        """
        self.parent = p

    def disownEventParent(self):
        """
        Unparent this event dispatcher.
        """
        self.parent = None
        return