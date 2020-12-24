# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/util/exception_handler.py
# Compiled at: 2020-04-13 02:37:12
# Size of source mod 2**32: 809 bytes
import time, logging
logger = logging.getLogger(__name__)

def retry(delays=(1, 3, 5), exception=Exception):

    def decorator(function):

        def wrapper(*args, **kwargs):
            cnt = 0
            for delay in delays + (None, ):
                try:
                    return function(*args, **kwargs)
                except exception as e:
                    try:
                        if delay is None:
                            logger.info('Retry failed after %d times.' % cnt)
                            raise
                        else:
                            cnt += 1
                            logger.info('Exception found on retry %d: -- retry after %ds' % (cnt, delay))
                            logger.exception(e)
                            time.sleep(delay)
                    finally:
                        e = None
                        del e

        return wrapper

    return decorator