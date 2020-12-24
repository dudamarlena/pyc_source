# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/marrow/util/object.py
# Compiled at: 2012-10-11 17:32:03
"""Object instance and class helper functions."""
import logging, inspect
from functools import partial
from marrow.util.compat import binary, unicode
__all__ = [
 'flatten', 'yield_property', 'yield_keyvalue', 'NoDefault', 'load_object', 'Cache', 'LoggingFile', 'CounterMeta']

def flatten(x):
    """flatten(sequence) -> list
    
    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).
    
    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]
    """
    for el in x:
        if hasattr(el, '__iter__') and not isinstance(el, (binary, unicode)):
            for els in flatten(el):
                yield els

        else:
            yield el


def yield_property(iterable, name, default=None):
    for i in iterable:
        yield getattr(i, name, default)


def yield_keyvalue(iterable, key, default=None):
    for i in iterable:
        yield i[key] if key in iterable else default


class _NoDefault(object):
    pass


NoDefault = _NoDefault()

def merge(s, t):
    """Merge dictionary t into s."""
    for k, v in t.items():
        if isinstance(v, dict):
            if k not in s:
                s[k] = v
                continue
            s[k] = merge(s[k], v)
            continue
        s[k] = v

    return s


def load_object(target):
    """This helper function loads an object identified by a dotted-notation string.
    
    For example:
    
        # Load class Foo from example.objects
        load_object('example.objects:Foo')
    """
    parts, target = target.split(':') if ':' in target else (target, None)
    module = __import__(parts)
    for part in parts.split('.')[1:] + ([target] if target else []):
        module = getattr(module, part)

    return module


class Cache(dict):
    """A least-recently-used (LRU) cache.
    
    Discards the least recently referenced object when full.
    
    Based on Python Cookbook contributions from multiple sources:
    
        * http://code.activestate.com/recipes/521871/
        * http://code.activestate.com/recipes/498110/
        * http://code.activestate.com/recipes/252524/
        * http://code.activestate.com/recipes/498245/
    
    And Genshi's LRUCache:
    
        http://genshi.edgewall.org/browser/trunk/genshi/util.py
    
    Warning: If memory cleanup is diabled this dictionary will leak.
    
    """

    class CacheElement(object):

        def __init__(self, key, value):
            self.previous = self.next = None
            self.key, self.value = key, value
            return

        def __repr__(self):
            return repr(self.value)

    def __init__(self, capacity):
        super(Cache, self).__init__()
        self.head = self.tail = None
        self.capacity = capacity
        return

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.key
            cur = cur.next

    def __getitem__(self, key):
        element = super(Cache, self).__getitem__(key)
        self._update(element)
        return element.value

    def __setitem__(self, key, value):
        try:
            element = super(Cache, self).__getitem__(key)
            element.value = value
            self._update(element)
        except KeyError:
            element = self.CacheElement(key, value)
            super(Cache, self).__setitem__(key, element)
            self._insert(element)

        self._restrict()

    def _insert(self, element):
        element.previous, element.next = None, self.head
        if self.head is not None:
            self.head.previous = element
        else:
            self.tail = element
        self.head = element
        return

    def _restrict(self):
        while len(self) > self.capacity:
            del self[self.tail.key]
            if self.tail != self.head:
                self.tail = self.tail.previous
                self.tail.next = None
            else:
                self.head = self.tail = None

        return

    def _update(self, element):
        if self.head == element:
            return
        else:
            previous = element.previous
            previous.next = element.next
            if element.next is not None:
                element.next.previous = previous
            else:
                self.tail = previous
            element.previous, element.next = None, self.head
            self.head.previous = self.head = element
            return


class LoggingFile(object):
    """A write-only file-like object that redirects to the standard Python logging module."""

    def __init__(self, logger=None, level=logging.ERROR):
        logger = logger if logger else logging.getLogger('logfile')
        self.logger = partial(logger.log, level)

    def write(self, text):
        self.logger(text)

    def writelines(self, lines):
        for line in lines:
            self.logger(line)

    def close(self, *args, **kw):
        """A no-op method used for several of the file-like object methods."""
        pass

    def next(self, *args, **kw):
        """An error-raising exception usedbfor several of the methods."""
        raise IOError('Logging files can not be read.')

    flush = close
    read = next
    readline = next
    readlines = next


class CounterMeta(type):
    """
    A simple meta class which adds a ``_counter`` attribute to the instances of
    the classes it is used on. This counter is simply incremented for each new
    instance.
    """
    counter = 0

    def __call__(self, *args, **kwargs):
        instance = type.__call__(self, *args, **kwargs)
        instance._counter = CounterMeta.counter
        CounterMeta.counter += 1
        return instance


def getargspec(obj):
    """An improved inspect.getargspec.
    
    Has a slightly different return value from the default getargspec.
    
    Returns a tuple of:
        required, optional, args, kwargs
        list, dict, bool, bool
    
    Required is a list of required named arguments.
    Optional is a dictionary mapping optional arguments to defaults.
    Args and kwargs are True for the respective unlimited argument type.
    """
    argnames, varargs, varkw, _defaults = (None, None, None, None)
    if inspect.isfunction(obj) or inspect.ismethod(obj):
        argnames, varargs, varkw, _defaults = inspect.getargspec(obj)
    else:
        if inspect.isclass(obj):
            if inspect.ismethoddescriptor(obj.__init__):
                argnames, varargs, varkw, _defaults = ([], False, False, None)
            else:
                argnames, varargs, varkw, _defaults = inspect.getargspec(obj.__init__)
        elif hasattr(obj, '__call__'):
            argnames, varargs, varkw, _defaults = inspect.getargspec(obj.__call__)
        else:
            raise TypeError('Object not callable?')
        if argnames and argnames[0] == 'self':
            del argnames[0]
        if _defaults is None:
            _defaults = []
            defaults = dict()
        else:
            defaults = dict()
            _defaults = list(_defaults)
            _defaults.reverse()
            argnames.reverse()
            for i, default in enumerate(_defaults):
                defaults[argnames[i]] = default

        argnames.reverse()
    return (
     argnames, defaults, True if varargs else False, True if varkw else False)