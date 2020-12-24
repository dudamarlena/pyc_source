# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/lib/orm/utils.py
# Compiled at: 2018-05-06 21:04:31
# Size of source mod 2**32: 615 bytes


class AsyncIterWrapper:
    __doc__ = 'Async wrapper for sync iterables\n\n    Copied from aitertools package.\n    '

    def __init__(self, iterable):
        self._it = iter(iterable)

    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._it)
        except StopIteration as e:
            raise StopAsyncIteration() from e

    def __repr__(self):
        return '<AsyncIterWrapper {}>'.format(self._it)


async def alist--- This code section failed: ---

 L.  25         0  LOAD_LISTCOMP            '<code_object <listcomp>>'
                2  LOAD_STR                 'alist.<locals>.<listcomp>'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  LOAD_FAST                'iterable'
                8  GET_AITER        
               10  LOAD_CONST               None
               12  YIELD_FROM       
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


async def anext(iterable):
    return await iterable.__anext__()