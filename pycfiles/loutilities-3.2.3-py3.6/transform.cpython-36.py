# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\transform.py
# Compiled at: 2019-11-20 14:58:11
# Size of source mod 2**32: 2988 bytes
from .csvu import str2num

class Transform:
    __doc__ = "\n    transform objects using a mapping object\n\n    mapping is dict like {'targetattr_n':'sourceattr_n', 'targetattr_m':f(source), ...}\n    if order of operation is importand use OrderedDict\n\n    source and target may be dict-like or class-like\n\n    :param mapping: mapping dict with key for each target attr, value is key in source or function(source)\n    :param sourceattr: True if getattr works with source, otherwise uses __getitem__ (as dict)\n    :param targetattr: True if setattr works with target, otherwise uses __setitem__ (as dict)\n    "

    def __init__(self, mapping, sourceattr=True, targetattr=True):
        self.mapping = mapping
        self.sourceattr = sourceattr
        self.targetattr = targetattr

    def transform(self, source, target):
        """
        set target values based on source object

        :param source: source object (dict-like or class-like)
        :param target: target object (dict-like or class-like)
        """
        for key in self.mapping:
            if hasattr(self.mapping[key], '__call__'):
                callback = self.mapping[key]
                value = callback(source)
            else:
                sourceattr = self.mapping[key]
                if self.sourceattr:
                    value = getattr(source, sourceattr)
                else:
                    value = source[sourceattr]
            if isinstance(value, str):
                value = str2num(value)
                if value in ('false', 'False'):
                    value = False
                elif value in ('true', 'True'):
                    value = True
            if self.targetattr:
                setattr(target, key, value)
            else:
                target[key] = value