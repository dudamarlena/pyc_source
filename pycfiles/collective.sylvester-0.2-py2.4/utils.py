# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/sylvester/utils.py
# Compiled at: 2009-07-12 11:14:11
from time import time

def _cache_key_base(fun, obj, *args, **kwargs):
    """  
    Generic cache key
    """
    s_args = str(args)
    li = kwargs.items()
    li.sort()
    s_kwargs = str(li)
    return '%s%s%s%s' % (fun.func_name, str(obj.context.getPhysicalPath()), s_args, s_kwargs)


def cache_key_3600(fun, obj, *args, **kwargs):
    result = _cache_key_base(fun, obj, *args, **kwargs)
    return '%s%s' % (result, time() // 3600)


def cache_key_60(fun, obj, *args, **kwargs):
    result = _cache_key_base(fun, obj, *args, **kwargs)
    return '%s%s' % (result, time() // 60)