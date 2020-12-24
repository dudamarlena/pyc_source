# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sflib/dictclass.py
# Compiled at: 2008-05-24 07:49:58
"""
python-sflib dictclass.py
"""

class Dictionary(object):
    """
    A base class that acts like a dictionary, but saving to instance
    variables.

       >>> d = Dictionary()

       >>> d['k1'] = 23

       >>> d['k1']
       23

       >>> d.var = 'hello'

       >>> d['var']
       'hello'

       >>> d.getdict()
       {'var': 'hello', 'k1': 23}
    """
    __module__ = __name__

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)

    def __setitem__(self, key, val):
        setattr(self, key, val)

    def getdict(self):
        d = dict()
        attrs = self.__dict__
        for k in attrs.keys():
            d[k] = attrs[k]

        return d