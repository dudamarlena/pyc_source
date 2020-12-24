# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/util.py
# Compiled at: 2013-04-04 15:36:36
import os, sys, locale, collections, paste.webkit
from babel.core import Locale, UnknownLocaleError

def sys_path_install():
    webware_dir = os.path.join(os.path.dirname(paste.webkit.__file__), 'FakeWebware')
    if webware_dir not in sys.path:
        sys.path.append(webware_dir)


def loadClass(className):
    return (lambda x: getattr(__import__(x.rsplit('.', 1)[0], fromlist=x.rsplit('.', 1)[0]), x.split('.')[(-1)]))(className)


def getSuperClass(cls):
    if len(cls.__mro__) > 1:
        return cls.__mro__[1]
    else:
        return


def clsname(cls):
    """@return: fully qualified name of given class"""
    return cls.__module__ + '.' + cls.__name__


def fullname(obj):
    """@return: fully qualified name of given object's class"""
    return clsname(obj.__class__)


def totalseconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1000000.0) / 1000000.0


def defaultLocale():
    try:
        lang, _ = locale.getdefaultlocale()
    except Exception:
        lang = None

    if lang is not None:
        try:
            return Locale.parse(lang)
        except UnknownLocaleError:
            pass

    else:
        try:
            return Locale.default()
        except UnknownLocaleError:
            return Locale('en', 'US')

    return


class EventObject(object):

    def __init__(self, source):
        self._source = source

    def getSource(self):
        return self._source


class IEventListener(object):
    pass


KEY, PREV, NEXT = range(3)

class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]
        self.map = {}
        if iterable is not None:
            self |= iterable
        return

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[PREV]
            curr[NEXT] = end[PREV] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, nxt = self.map.pop(key)
            prev[NEXT] = nxt
            nxt[PREV] = prev

    def __iter__(self):
        end = self.end
        curr = end[NEXT]
        while curr is not end:
            yield curr[KEY]
            curr = curr[NEXT]

    def __reversed__(self):
        end = self.end
        curr = end[PREV]
        while curr is not end:
            yield curr[KEY]
            curr = curr[PREV]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = next(reversed(self)) if last else next(iter(self))
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

    def __del__(self):
        self.clear()