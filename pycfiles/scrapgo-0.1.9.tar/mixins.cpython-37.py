# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\modules\request\mixins.py
# Compiled at: 2019-05-23 16:06:28
# Size of source mod 2**32: 1030 bytes
import functools
from collections import abc
from scrapgo import settings

class RequestMixin(object):
    RETRY_INTERVAL_SECONDS = settings.RETRY_INTERVAL_SECONDS

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)

    @classmethod
    def retry(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(self.RETRY_INTERVAL_SECONDS, abc.Iterable):
                for i, sec in enumerate(self.RETRY_INTERVAL_SECONDS):
                    try:
                        r = func(*args, **kwargs)
                    except:
                        message = 'Request Failed, retry after {}sec(trys: {})'.format(sec, i + 1)
                        print(message)
                        time.sleep(sec)
                    else:
                        return r

            else:
                r = func(*args, **kwargs)
            return r

        return wrapper