# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mathml/pmathml/events.py
# Compiled at: 2004-10-05 18:16:46
import weakref

class EventSource(object):
    """A GObject-like signal framework"""

    def __init__(self):
        self.__connections = {}

    def connect(self, name, handler, data=None):
        try:
            l = self.__connections[name]
        except KeyError:
            l = []
            self.__connections[name] = l

        item = weakref.ref(handlerobject)
        l.append((handler, data))

    def emit(self, name, args):
        try:
            l = self.__connections[name]
        except KeyError:
            return

        for (handler, data) in l:
            _handler = handler()
            if _handler is None:
                l.remove((handler, data))
                continue
            _args = [
             self] + args
            if data is not None:
                _args.append(data)
            _handler(*_args)

        return