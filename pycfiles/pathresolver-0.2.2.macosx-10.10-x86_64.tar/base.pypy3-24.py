# uncompyle6 version 3.7.4
# PyPy Python bytecode 3.2 (3187)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrewcrosio/projects/pathresolver/pypy3/site-packages/pathresolver/resolver/base.py
# Compiled at: 2015-04-17 13:50:21
import abc

class ResolverBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def resolve(self, key, value):
        raise NotImplementedError()

    def __call__(self, key, value):
        return self.resolve(key, value)