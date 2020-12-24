# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Brian/Work/github_projects/marvin_pypi/python/marvin/extern/marvin_brain/python/brain/core/core.py
# Compiled at: 2018-01-12 14:08:14
# Size of source mod 2**32: 1009 bytes
from __future__ import division
from __future__ import print_function
from brain.core.exceptions import BrainError

class URLMapDict(dict):
    __doc__ = 'A custom dictionary for urlmap that fails with a custom error.'

    def __init__(self, inp={}):
        (self.update)(**dict(((kk, self.parse(vv)) for kk, vv in inp.items())))

    @classmethod
    def parse(cls, vv):
        if isinstance(vv, dict):
            return cls(vv)
        else:
            if isinstance(vv, list):
                return [cls.parse(ii) for ii in vv]
            return vv

    def __missing__(self, key):
        """Overrides the default KeyError exception."""
        if len(self.keys()) == 0:
            raise BrainError('No URL Map found. Cannot make remote call')
        else:
            raise BrainError('Key {0} not found in urlmap.'.format(key))