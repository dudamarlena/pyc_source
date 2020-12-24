# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pysecret-project/pysecret/singleton_alternative.py
# Compiled at: 2019-04-10 20:34:51
# Size of source mod 2**32: 1236 bytes
import weakref

class CachedSpamManager(object):
    """CachedSpamManager"""
    cached_klass = None

    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def new(self, name, *args, **kwargs):
        """
        Factory method.
        """
        if name not in self._cache:
            temp = self.cached_klass._new(name, *args, **kwargs)
            self._cache[name] = temp
        else:
            temp = self._cache[name]
        return temp

    def clear(self):
        self._cache.clear()


class Spam(object):

    def __init__(self, name, *args, **kwargs):
        msg = "Can't instantiate directly, use Cached{}Manager.new(name, ...) instead.".format(self.__class__.__name__)
        raise RuntimeError(msg)

    @classmethod
    def _new(cls, name, *args, **kwargs):
        """
        User custom instance constructor.

        implement constructor this way::

            def _new(cls, name, *args, **kwargs):
                self = cls.__new__(cls)
                # put __init__(...) logic here
                self.name = name
                return self
        """
        raise NotImplementedError