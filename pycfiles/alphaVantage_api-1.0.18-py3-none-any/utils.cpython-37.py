# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\appli\Documents\GitHub\AlphaVantageAPI\alphaVantageAPI\utils.py
# Compiled at: 2019-09-29 14:24:31
# Size of source mod 2**32: 1270 bytes
import time
from functools import wraps
from pathlib import Path

def timed(fn):
    """Simple timing decorator that stores the elapsed time
    as a string property called 'timed' to the fn.
    """

    @wraps(fn)
    def _timer(*args, **kwargs):
        start = time.time()
        fn(*args, **kwargs)
        end = time.time()
        diff = end - start
        elapsed_time = f"[!] {fn.__name__} {diff * 1000:2.2f} ms ({diff:2.2f} s)"
        fn.timed = elapsed_time
        return fn

    return _timer


def is_home(path: Path):
    """Determines if the path is a User path or not.
    If the Path begins with '~', then True, else False"""
    if isinstance(path, str):
        if len(path) > 0:
            path = Path(path)
    if isinstance(path, Path):
        if len(path.parts) > 0:
            return path.parts[0] == '~'
    return False