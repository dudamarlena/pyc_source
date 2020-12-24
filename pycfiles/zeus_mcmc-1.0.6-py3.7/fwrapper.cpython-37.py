# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zeus/fwrapper.py
# Compiled at: 2020-01-05 09:20:49
# Size of source mod 2**32: 672 bytes
import numpy as np

class _FunctionWrapper(object):
    __doc__ = '\n    This is a hack to make the likelihood function pickleable when ``args``\n    or ``kwargs`` are also included.\n\n    Args:\n        f (callable) : Log Probability function.\n        args (list): Extra arguments to be passed into the logprob.\n        kwargs (dict): Extra arguments to be passed into the logprob.\n\n    Returns:\n        Log Probability function.\n    '

    def __init__(self, f, args, kwargs):
        self.f = f
        self.args = [] if args is None else args
        self.kwargs = {} if kwargs is None else kwargs

    def __call__(self, x):
        return (self.f)(x, *(self.args), **self.kwargs)