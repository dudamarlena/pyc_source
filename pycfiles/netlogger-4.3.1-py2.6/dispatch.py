# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/dispatch.py
# Compiled at: 2010-06-05 00:42:59
"""
Framework to dispatch and handle events (dictionaries).

Example usage:

>>> class PrintStuff:
...     def print_name(self, event):
...        print(event['name'])
>>> ps = PrintStuff()
>>> # Match all events with field 'name' ending in 'Gunter'
>>> hndlr1 = RegexMatchHandler({"name":".*Gunter"}, method=ps.print_name)
>>> # Match all events with field 'name' starting with 'Dan'
>>> hndlr2 = RegexMatchHandler({"name":"Dan.*"}, method=ps.print_name)
>>> disp = Dispatcher()
>>> disp.register(hndlr1)
'handler.1'
>>> disp.register(hndlr2)
'handler.2'
>>> disp.dispatch({"message":"hello"}) # no match
>>> disp.dispatch({"name":"hello"}) # no match
>>> disp.dispatch({"name":"Dan Gunter"}) # 2 matches
Dan Gunter
Dan Gunter
>>> disp.dispatch({"name":"Mr. Gunter"}) # 1 match
Mr. Gunter
>>> disp.remove("handler.1") # remove by id
True
>>> disp.remove(hndlr2) # remove by instance
True
"""
__author__ = 'dang'
__rcsid__ = '$Id: dispatch.py 24857 2010-06-05 04:41:51Z dang $'
import Queue, re, threading
from nllog import DoesLogging
from nlapi import EVENT_FIELD

class Dispatcher(DoesLogging):
    """Send events to interested handlers.
    """
    ID_PREFIX = 'handler'

    def __init__(self):
        DoesLogging.__init__(self)
        self._handlers = []
        self._prehandle_fn = None
        if self._dbg:
            self._count = 0
        return

    def dispatch(self, event):
        """Dispatch event record to registered handlers.
        """
        if self._prehandle_fn:
            hevent = self._prehandle_fn(event)
        else:
            hevent = event
        for (id_, handler) in self._handlers:
            if handler.match(event):
                if self._dbg:
                    self._count += 1
                    self.log.debug('dispatched_event', handler__id=id_, name=event[EVENT_FIELD])
                handler.handle(hevent)

    def register(self, handler):
        """Add a handler, returning a string identifier that
        can be passed to remove(). Idempotent.
        """
        idx = self._find(handler)
        if idx > -1:
            return self._handlers[idx][0]
        new_id = '%s.%d' % (self.ID_PREFIX, len(self._handlers) + 1)
        self._handlers.append((new_id, handler))
        return new_id

    def remove(self, handler):
        idx, removed = self._find(handler), False
        if idx >= 0:
            del self._handlers[idx]
            removed = True
        return removed

    def set_prehandle(self, fn):
        """Set a function to be applied to event dictionaries
        before they are passed in to handlers for handling
        (not for matching).
        """
        self._prehandle_fn = fn

    def _find(self, handler_or_id):
        """Return index if the given handler or id exists, or -1
        """
        for (idx, (id_, inst)) in enumerate(self._handlers):
            if handler_or_id == id_ or handler_or_id == inst:
                return idx

        return -1


class Handler:
    """Base class to handle a dispatched event."""

    def __init__(self, method=None):
        self._handler_method = method

    def set_method(self, method):
        """Allows behavior to be plugged in without inheritance."""
        self._handler_method = method

    def handle(self, event):
        return self._handler_method(event)

    def match(self, event):
        return False


class EventPrefixMatchHandler(Handler):
    """Match incoming events on one or more event name prefixes.
    """

    def __init__(self, event_keyword='event', **kw):
        """Constructor.
        
        :Parameters:
          keyword - Event name keyword in dictionary (string)
        """
        Handler.__init__(self, **kw)
        self._prefixes = []
        self._keyword = event_keyword

    def add_prefix(self, prefix):
        """Add an event prefix to match on.

        :Parameters:
          prefix - Event prefix (string)
        """
        self._prefixes.append(prefix)

    def match(self, event):
        """Match event against one of the event prefixes.
        """
        event_name = event.get(self._keyword, None)
        if event_name is not None:
            if not self._prefixes:
                return True
            for prefix in self._prefixes:
                if event_name.startswith(prefix):
                    return True

        return False


class RegexMatchHandler(Handler):
    """Match incoming events using a dictionary of regular expressions
    """

    def __init__(self, expr_dict, search=False, **kw):
        """Set regular expression to match on.
        
        If 'search' is True, then match anywhere in the string,
        otherwise only match from the beginning of the string.
        """
        self._search = search
        self._edict = {}
        for (key, value) in expr_dict.items():
            self._edict[key] = re.compile(value)

        Handler.__init__(self, **kw)

    def match(self, event):
        """Attempt to match name, value pairs in event.
        """
        for (name, expr) in self._edict.items():
            if not event.has_key(name):
                return False
            if self._search:
                matched = expr.search(event[name])
            else:
                matched = expr.match(event[name])
            if not matched:
                return False

        return True


class HandlerThread(threading.Thread):
    """Make handlers run in their own thread.
    This allows them to return immediately from the handle() method,
    instead of running that code synchronously.

    Usage example:
    >>> class PrintStuff:
    ...     def print_name(self, event):
    ...        print(event['name'])
    >>> ps = PrintStuff()
    >>> # Match all events with field 'name' ending in 'Gunter'
    >>> h1 = RegexMatchHandler({"name":".*Gunter"})
    >>> h1.set_method(ps.print_name)
    >>> th1 = HandlerThread(h1)
    >>> th1.start()
    >>> disp = Dispatcher()
    >>> disp.register(h1)
    'handler.1'
    >>> disp.dispatch({"message":"hello"}) # no match
    >>> disp.dispatch({"name":"hello"}) # no match
    >>> disp.dispatch({"name":"Dan Gunter"}) # 1 match
    Dan Gunter
    >>> disp.remove(h1)
    >>> th1.stop()
    >>> disp.dispatch({"name":"Dan Gunter"}) # nothing, now
    """
    READ_TIMEOUT = 1

    def __init__(self, handler):
        """Set up to run in thread.
        """
        self.__handle = handler.handle
        self._handler.set_method(self.handle)
        self._queue = Queue.Queue()
        self._done = False
        threading.Thread.__init__(target=self.run)

    def handle(self, event):
        self._queue.put(event)

    def run(self):
        while not self._done:
            event = self._queue.get(True, self.READ_TIMEOUT)
            self.__handle(event)

    def stop(self):
        self._done = True
        self.join(2 * self.READ_TIMEOUT)


if __name__ == '__main__':
    import doctest
    doctest.testmod()