# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/comparsion.py
# Compiled at: 2012-06-09 18:49:08
__all__ = ('ComparsionMixin', )

class ComparsionMixin(object):
    """
    Mixin to help compare two instances
    """

    def __cmp__(self, other):
        """
        Compare two items
        """
        if other == None:
            return -1
        else:
            if self.body != None and other.body != None and set(self.body).symmetric_difference(other.body) not in [
             self.IGNORE_KEYS, set([])]:
                return -1
            if self.body != None and self.body == other.body:
                for key in other.body.keys():
                    if key in self.IGNORE_KEYS:
                        continue
                    if self.body.get('key', None) != other.body.get('key', None):
                        return -1

            if self.body == None and self.body != other.body:
                return -1
            if self.id == other.id and self.rev == other.rev:
                return 0
            return -1