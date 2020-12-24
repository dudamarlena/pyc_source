# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/diogo.mmartins/venvs/reloadable2.7/lib/python2.7/site-packages/reloadable/decorators.py
# Compiled at: 2018-03-06 13:40:53
from functools import wraps, partial
from time import sleep
from reloadable import config

def reloadable(exception_callback=None, sleep_time=0, stop_condition_exception=None, max_reloads=None, return_on_success=False):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            reload_counter = 0
            if not config.ENABLED:
                return func(*args, **kwargs)
            else:
                last_exception = None
                while reload_counter != max_reloads:
                    try:
                        result = func(*args, **kwargs)
                        last_exception = None
                        if return_on_success:
                            return result
                    except stop_condition_exception or config.STOP_CONDITION_EXCEPTION as e:
                        raise e
                    except Exception as e:
                        if exception_callback:
                            exception_callback(e)
                        sleep(sleep_time)
                        reload_counter += 1
                        last_exception = e

                if last_exception:
                    raise last_exception
                return

        return wrapper

    return decorator


retry_on_error = partial(reloadable, return_on_success=True)