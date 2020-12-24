# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/api/utils/profile_util.py
# Compiled at: 2020-05-02 23:16:48
# Size of source mod 2**32: 1221 bytes
import time
from arch.api.utils import log_utils
import inspect
from functools import wraps
LOGGER = log_utils.getLogger('PROFILING')

def log_elapsed(func):
    func_name = func.__name__

    @wraps(func)
    def _fn(*args, **kwargs):
        t = time.time()
        name = f"{func_name}#{kwargs['func_tag']}" if 'func_tag' in kwargs else func_name
        rtn = func(*args, **kwargs)
        frame = inspect.getouterframes(inspect.currentframe(), 2)
        LOGGER.debug(f"{frame[1].filename.split('/')[(-1)]}:{frame[1].lineno} call {name}, takes {time.time() - t}s")
        return rtn

    return _fn