# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/mixins.py
# Compiled at: 2013-03-08 14:06:20
# Size of source mod 2**32: 2006 bytes
__all__ = ('ComparsionMixin', 'LazyLoadMixin')

class ComparsionMixin(object):
    """ComparsionMixin"""

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
                if self.body is not None and other.body is not None:
                    for key in keys(other):
                        if self.body.get(key, None) != other.body.get(key, None):
                            return False

                if self._id is not None and self._rev is not None and (self._id != other._id or str(self._rev) != str(other._rev)):
                    pass
                return False
            return True


class LazyLoadMixin(object):
    """LazyLoadMixin"""

    def __getattribute__(self, name):
        """Fetching lazy document"""
        if name in object.__getattribute__(self, 'LAZY_LOAD_HANDLERS'):
            object.__getattribute__(self, '_handle_lazy')()
        return object.__getattribute__(self, name)

    def _handle_lazy(self):
        if self._lazy_loaded is False:
            self._lazy_loaded = True
            self.lazy_loader()