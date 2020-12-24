# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jojo/.virtualenvs/apikit/lib/python3.6/site-packages/apikit/cache.py
# Compiled at: 2018-08-06 13:02:15
# Size of source mod 2**32: 857 bytes
import types
from hashlib import sha1

def cache_hash(*a, **kw):
    """ Try to hash an arbitrary object for caching. """

    def cache_str(o):
        if isinstance(o, (types.FunctionType, types.BuiltinFunctionType,
         types.MethodType, types.BuiltinMethodType,
         types.UnboundMethodType)):
            return getattr(o, 'func_name', 'func')
        else:
            if isinstance(o, dict):
                o = [k + ':' + cache_str(v) for k, v in o.items()]
            else:
                if isinstance(o, (list, tuple, set)):
                    o = sorted(map(cache_str, o))
                    o = '|'.join(o)
                if isinstance(o, basestring):
                    return o
                if hasattr(o, 'updated_at'):
                    return cache_str((repr(o), o.updated_at))
            return repr(o)

    hash = cache_str((a, kw)).encode('utf-8')
    return sha1(hash).hexdigest()