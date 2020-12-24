# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/libs/rediskit/base.py
# Compiled at: 2016-02-25 04:17:16
from itertools import chain

class RedisKit(object):

    @classmethod
    def factory(cls, *base_args, **base_kwargs):

        def constructor(*args, **kwargs):
            kwargs.update(base_kwargs)
            return cls(*chain(base_args, args), **kwargs)

        return constructor