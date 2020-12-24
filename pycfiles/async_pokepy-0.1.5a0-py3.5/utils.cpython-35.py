# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/async_pokepy/utils.py
# Compiled at: 2019-05-20 16:37:56
# Size of source mod 2**32: 2827 bytes
"""
The MIT License (MIT)

Copyright (c) 2019 Lorenzo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import functools, warnings
from inspect import isawaitable
from typing import Union
from urllib.parse import quote
try:
    from lru import LRU
except ImportError:
    LRU = None

__all__ = ()

def _fmt_param(thing: Union[(int, str)]) -> str:
    if isinstance(thing, int):
        return str(thing)
    return quote('-'.join(thing.lower().split()), safe='')


def _pretty_format(thing: str) -> str:
    if thing.lower() in ('oh-ho', 'porygon-z'):
        return thing.capitalize()
    return thing.replace('-', ' ').title()


def _make_cache_key(key):
    if isinstance(key, str):
        if key.isdigit():
            return int(key)
        return _fmt_param(key)
    return key


def cached(maxsize: int, with_name: bool=True):

    def outer--- This code section failed: ---

 L.  66         0  LOAD_GLOBAL              functools
                3  LOAD_ATTR                wraps
                6  LOAD_DEREF               'func'
                9  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L.  67        12  LOAD_GLOBAL              Union
               15  LOAD_GLOBAL              int
               18  LOAD_GLOBAL              str
               21  BUILD_TUPLE_2         2 
               24  BINARY_SUBSCR    
               25  LOAD_CONST               ('query',)
               28  LOAD_CLOSURE             'cache'
               31  LOAD_CLOSURE             'func'
               34  LOAD_CLOSURE             'with_name'
               37  BUILD_TUPLE_3         3 
               40  LOAD_CODE                <code_object inner>
               43  LOAD_STR                 'cached.<locals>.outer.<locals>.inner'
               46  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               52  CALL_FUNCTION_1       1  '1 positional, 0 named'
               55  STORE_FAST               'inner'

 L.  82        58  LOAD_GLOBAL              LRU
               61  POP_JUMP_IF_FALSE    79  'to 79'

 L.  83        64  LOAD_GLOBAL              LRU
               67  LOAD_DEREF               'maxsize'
               70  CALL_FUNCTION_1       1  '1 positional, 0 named'
               73  STORE_DEREF              'cache'
               76  JUMP_FORWARD         98  'to 98'
               79  ELSE                     '98'

 L.  85        79  BUILD_MAP_0           0 
               82  STORE_DEREF              'cache'

 L.  86        85  LOAD_GLOBAL              warnings
               88  LOAD_ATTR                warn
               91  LOAD_STR                 'lru-dict is not installed, so the cache will not have a maxsize.'
               94  CALL_FUNCTION_1       1  '1 positional, 0 named'
               97  POP_TOP          
             98_0  COME_FROM            76  '76'

 L.  88        98  LOAD_DEREF               'cache'
              101  LOAD_FAST                'inner'
              104  STORE_ATTR               cache

 L.  90       107  LOAD_FAST                'inner'
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `MAKE_CLOSURE_A_2_0' instruction at offset 46

    return outer


async def maybe_coroutine(f, *args, **kwargs):
    value = f(*args, **kwargs)
    if isawaitable(value):
        return await value
    return value