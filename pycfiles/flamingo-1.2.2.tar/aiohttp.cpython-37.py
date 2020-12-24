# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/utils/aiohttp.py
# Compiled at: 2020-04-28 06:15:31
# Size of source mod 2**32: 347 bytes
from functools import wraps

def no_cache():

    def wrapper(coroutine):

        @wraps(coroutine)
        async def wrapped(*args):
            response = await coroutine(*args)
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return response

        return wrapped

    return wrapper