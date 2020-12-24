# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pysecret-project/pysecret/singleton_alternative.py
# Compiled at: 2019-04-10 20:34:51
# Size of source mod 2**32: 1236 bytes
import weakref

class CachedSpamManager(object):
    __doc__ = '\n    Instance cache manager.\n    '
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