# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: graphdash/struct/defaulttransformdict.py
# Compiled at: 2019-04-25 09:26:58
from .transformdict import TransformDict

class DefaultTransformDict(TransformDict):

    def __init__(self, default_factory=None, *args, **kwargs):
        if default_factory is not None and not callable(default_factory):
            raise TypeError('first argument must be callable')
        super(DefaultTransformDict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory
        return

    def __getitem__(self, key):
        try:
            return super(DefaultTransformDict, self).__getitem__(key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value