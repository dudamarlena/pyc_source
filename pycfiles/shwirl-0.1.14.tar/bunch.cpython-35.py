# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/util/bunch.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 420 bytes


class SimpleBunch(dict):
    __doc__ = ' Container object for datasets: dictionnary-like object that\n        exposes its keys as attributes.\n    '

    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self