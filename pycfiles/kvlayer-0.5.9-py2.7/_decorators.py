# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/_decorators.py
# Compiled at: 2015-07-31 13:31:44
import time, logging
from functools import wraps

def retry(retry_exceptions=[
 Exception], retry_attempts=3):
    """
    Configurable decorator that will retry after intermittent failures.

    @type retry_exceptions: list
    @param retry_exceptions: List of exceptions that will be retried.

    @type retry_attempts: integer
    @param retry_attempts: Number of times to retry a function after it has failed
    """

    def decorator(method):

        @wraps(method)
        def wrapper(*args, **kwargs):
            tries = 0
            while 1:
                try:
                    tries += 1
                    return method(*args, **kwargs)
                    break
                except Exception as exc:
                    if not any([ isinstance(exc, e) for e in retry_exceptions ]) or tries > retry_attempts:
                        raise
                    else:
                        logging.warn('Retrying because of exception', exc_info=True)
                        time.sleep(3 * tries)

        return wrapper

    return decorator