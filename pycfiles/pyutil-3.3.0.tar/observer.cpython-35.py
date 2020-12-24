# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/observer.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 3145 bytes
from twisted.internet import defer
try:
    from foolscap.eventual import eventually
    eventually
except ImportError:
    from twisted.internet import reactor

    def eventually(f, *args, **kwargs):
        return reactor.callLater(0, f, *args, **kwargs)


class OneShotObserverList:
    __doc__ = 'A one-shot event distributor.'

    def __init__(self):
        self._fired = False
        self._result = None
        self._watchers = []

    def __repr__(self):
        if self._fired:
            return '<OneShotObserverList -> %s>' % (self._result,)
        else:
            return '<OneShotObserverList [%s]>' % (self._watchers,)

    def _get_result(self):
        return self._result

    def when_fired(self):
        if self._fired:
            return defer.succeed(self._get_result())
        d = defer.Deferred()
        self._watchers.append(d)
        return d

    def fire(self, result):
        assert not self._fired
        self._fired = True
        self._result = result
        self._fire(result)

    def _fire(self, result):
        for w in self._watchers:
            eventually(w.callback, result)

        del self._watchers

    def fire_if_not_fired(self, result):
        if not self._fired:
            self.fire(result)


class LazyOneShotObserverList(OneShotObserverList):
    __doc__ = '\n    a variant of OneShotObserverList which does not retain\n    the result it handles, but rather retains a callable()\n    through which is retrieves the data if and when needed.\n    '

    def __init__(self):
        OneShotObserverList.__init__(self)

    def _get_result(self):
        return self._result_producer()

    def fire(self, result_producer):
        """
        @param result_producer: a no-arg callable which
        returns the data which is to be considered the
        'result' for this observer list.  note that this
        function may be called multiple times - once
        upon initial firing, and potentially once more
        for each subsequent when_fired() deferred created
        """
        assert not self._fired
        self._fired = True
        self._result_producer = result_producer
        if self._watchers:
            self._fire(self._get_result())


class ObserverList:
    __doc__ = 'A simple class to distribute events to a number of subscribers.'

    def __init__(self):
        self._watchers = []

    def subscribe(self, observer):
        self._watchers.append(observer)

    def unsubscribe(self, observer):
        self._watchers.remove(observer)

    def notify(self, *args, **kwargs):
        for o in self._watchers:
            eventually(o, *args, **kwargs)