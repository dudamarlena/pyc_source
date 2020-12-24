# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/torchreinforce/distributions/wrapper.py
# Compiled at: 2019-01-18 12:13:06
# Size of source mod 2**32: 377 bytes
from .base import ReinforceDistribution

def getNonDeterministicWrapper(baseClass):

    class NonDeterministicWrapper(baseClass):

        def __init__(self, *args, **kwargs):
            if 'deterministic' in kwargs:
                del kwargs['deterministic']
            (super(NonDeterministicWrapper, self).__init__)(*args, **kwargs)

    return NonDeterministicWrapper