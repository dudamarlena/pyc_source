# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/marrow/util/patterns.py
# Compiled at: 2012-07-26 02:07:58
__all__ = [
 'Borg']

class Borg(object):
    """The Borg are better than Singletons.
    
    Create instances that have the same underlying dictionary.
    
    Popeye says: "You will be askimilgrated."
    """
    _dict = {}

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls, *args, **kwds)
        obj.__dict__ = cls._dict
        return obj