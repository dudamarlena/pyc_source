# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/utils.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 6359 bytes
from __future__ import unicode_literals
import inspect, os, signal, sys, threading, weakref
from wcwidth import wcwidth
from six.moves import range
__all__ = ('Event', 'DummyContext', 'get_cwidth', 'suspend_to_background_supported',
           'is_conemu_ansi', 'is_windows', 'in_main_thread', 'take_using_weights',
           'test_callable_args')

class Event(object):
    __doc__ = '\n    Simple event to which event handlers can be attached. For instance::\n\n        class Cls:\n            def __init__(self):\n                # Define event. The first parameter is the sender.\n                self.event = Event(self)\n\n        obj = Cls()\n\n        def handler(sender):\n            pass\n\n        # Add event handler by using the += operator.\n        obj.event += handler\n\n        # Fire event.\n        obj.event()\n    '

    def __init__(self, sender, handler=None):
        self.sender = sender
        self._handlers = []
        if handler is not None:
            self += handler

    def __call__(self):
        """ Fire event. """
        for handler in self._handlers:
            handler(self.sender)

    def fire(self):
        """ Alias for just calling the event. """
        self()

    def __iadd__(self, handler):
        """
        Add another handler to this callback.
        (Handler should be a callable that takes exactly one parameter: the
        sender object.)
        """
        assert callable(handler)
        if not test_callable_args(handler, [None]):
            raise TypeError("%r doesn't take exactly one argument." % handler)
        self._handlers.append(handler)
        return self

    def __isub__(self, handler):
        """
        Remove a handler from this callback.
        """
        self._handlers.remove(handler)
        return self


_signatures_cache = weakref.WeakKeyDictionary()

def test_callable_args(func, args):
    """
    Return True when this function can be called with the given arguments.
    """
    if not isinstance(args, (list, tuple)):
        raise AssertionError
    else:
        signature = getattr(inspect, 'signature', None)
        if signature is not None:
            try:
                sig = _signatures_cache[func]
            except KeyError:
                sig = signature(func)
                _signatures_cache[func] = sig

            try:
                (sig.bind)(*args)
            except TypeError:
                return False
            else:
                return True
        else:
            spec = inspect.getargspec(func)

            def drop_self(spec):
                args, varargs, varkw, defaults = spec
                if args[0:1] == ['self']:
                    args = args[1:]
                return inspect.ArgSpec(args, varargs, varkw, defaults)

            spec = drop_self(spec)
            if spec.varargs is not None:
                return True
            else:
                return len(spec.args) - len(spec.defaults or []) <= len(args) <= len(spec.args)


class DummyContext(object):
    __doc__ = '\n    (contextlib.nested is not available on Py3)\n    '

    def __enter__(self):
        pass

    def __exit__(self, *a):
        pass


class _CharSizesCache(dict):
    __doc__ = '\n    Cache for wcwidth sizes.\n    '

    def __missing__(self, string):
        if len(string) == 1:
            result = max(0, wcwidth(string))
        else:
            result = sum(max(0, wcwidth(c)) for c in string)
        if len(string) < 256:
            self[string] = result
        return result


_CHAR_SIZES_CACHE = _CharSizesCache()

def get_cwidth(string):
    """
    Return width of a string. Wrapper around ``wcwidth``.
    """
    return _CHAR_SIZES_CACHE[string]


def suspend_to_background_supported():
    """
    Returns `True` when the Python implementation supports
    suspend-to-background. This is typically `False' on Windows systems.
    """
    return hasattr(signal, 'SIGTSTP')


def is_windows():
    """
    True when we are using Windows.
    """
    return sys.platform.startswith('win')


def is_conemu_ansi():
    """
    True when the ConEmu Windows console is used.
    """
    return is_windows() and os.environ.get('ConEmuANSI', 'OFF') == 'ON'


def in_main_thread():
    """
    True when the current thread is the main thread.
    """
    return threading.current_thread().__class__.__name__ == '_MainThread'


def take_using_weights(items, weights):
    """
    Generator that keeps yielding items from the items list, in proportion to
    their weight. For instance::

        # Getting the first 70 items from this generator should have yielded 10
        # times A, 20 times B and 40 times C, all distributed equally..
        take_using_weights(['A', 'B', 'C'], [5, 10, 20])

    :param items: List of items to take from.
    :param weights: Integers representing the weight. (Numbers have to be
                    integers, not floats.)
    """
    if not isinstance(items, list):
        raise AssertionError
    else:
        if not isinstance(weights, list):
            raise AssertionError
        else:
            assert all(isinstance(i, int) for i in weights)
            assert len(items) == len(weights)
        assert len(items) > 0
    already_taken = [0 for i in items]
    item_count = len(items)
    max_weight = max(weights)
    i = 0
    while True:
        adding = True
        while adding:
            adding = False
            for item_i, item, weight in zip(range(item_count), items, weights):
                if already_taken[item_i] < i * weight / float(max_weight):
                    yield item
                    already_taken[item_i] += 1
                    adding = True

        i += 1