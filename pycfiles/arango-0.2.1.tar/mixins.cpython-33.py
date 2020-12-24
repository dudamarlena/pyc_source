# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/mixins.py
# Compiled at: 2013-03-08 14:06:20
# Size of source mod 2**32: 2006 bytes
__all__ = ('ComparsionMixin', 'LazyLoadMixin')

class ComparsionMixin(object):
    __doc__ = '\n    Mixin to help compare two instances\n    '

    def __eq__(self, other):
        """
        Compare two items
        """
        if not issubclass(type(other), self.__class__):
            return False
        else:
            if self.body == other.body and self._id == other._id and self._rev == other._rev:
                return True
            else:
                keys = lambda o: [key for key in o.body.keys() if key not in self.IGNORE_KEYS]
                if keys(self) != keys(other):
                    return False
                if self.body is not None:
                    if other.body is not None:
                        for key in keys(other):
                            if self.body.get(key, None) != other.body.get(key, None):
                                return False

                if self._id is not None and self._rev is not None and (self._id != other._id or str(self._rev) != str(other._rev)):
                    pass
                return False
            return True


class LazyLoadMixin(object):
    __doc__ = '\n    Mixin to lazily load some objects\n    before processing some of methods.\n\n    Required attributes:\n\n     * LAZY_LOAD_HANDLERS - list of methods which should be handled\n     * lazy_loader - method which should check status of loading\n                      and make decision about loading something\n                      or simply process next method in chain\n     * _lazy_loaded - property which provide status of the lazy loading,\n                      should be False by default\n    '

    def __getattribute__(self, name):
        """Fetching lazy document"""
        if name in object.__getattribute__(self, 'LAZY_LOAD_HANDLERS'):
            object.__getattribute__(self, '_handle_lazy')()
        return object.__getattribute__(self, name)

    def _handle_lazy(self):
        if self._lazy_loaded is False:
            self._lazy_loaded = True
            self.lazy_loader()