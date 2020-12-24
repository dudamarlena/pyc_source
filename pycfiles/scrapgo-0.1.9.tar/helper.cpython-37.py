# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\modules\request\helper.py
# Compiled at: 2019-05-26 03:36:33
# Size of source mod 2**32: 823 bytes
import time, functools
from collections import abc

def retry(func):

    @functools.wraps(func)
    def wrapper(self, url, **kwargs):
        if isinstance(self.RETRY_INTERVAL_SECONDS, abc.Iterable):
            for i, sec in enumerate(self.RETRY_INTERVAL_SECONDS):
                try:
                    r = func(self, url, **kwargs)
                except Exception as e:
                    try:
                        print('exception', e)
                        err = f"Request {url} Failed, retry after {sec}sec(trys: {i + 1})"
                        print(err)
                        time.sleep(sec)
                    finally:
                        e = None
                        del e

                else:
                    return r
            else:
                raise Exception(f"Request {url} Failed!")

        else:
            r = func(self, *args, **kwargs)
        return r

    return wrapper