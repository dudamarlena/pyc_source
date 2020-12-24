# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\types.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 1249 bytes
from random import Random

class RandomWithSeed(Random):
    __doc__ = 'A subclass of Random designed to expose the seed it was initially\n    provided with.\n\n    We consistently use this instead of Random objects because it makes\n    examples much easier to recreate.\n    '

    def __init__(self, seed):
        super().__init__(seed)
        self.seed = seed

    def __copy__(self):
        result = RandomWithSeed(self.seed)
        result.setstate(self.getstate())
        return result

    def __deepcopy__(self, table):
        return self.__copy__()

    def __repr__(self):
        return 'RandomWithSeed(%s)' % (self.seed,)