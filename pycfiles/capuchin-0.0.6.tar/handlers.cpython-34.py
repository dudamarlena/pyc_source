# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/py/capuchin/capuchin/handlers.py
# Compiled at: 2015-01-27 16:55:15
# Size of source mod 2**32: 4333 bytes
import concurrent.futures, functools, json, time, sys, time
from timeit import timeit
from tornado.web import RequestHandler
import hancock

def signed_log(key_func, log_func, expire_seconds=10):
    """Same as `signed` except the given `log_func` is used in place of stdout.
    """

    def decorator(fn):

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            handler = args[0]
            key = handler.get_query_argument('apikey')
            if not key:
                handler.set_status(401)
                return
            p_key = key_func(key)
            if not p_key:
                handler.set_status(401)
                log_func('No private key for:', key)
                return
            r = handler.request
            status_code, message = hancock.validate(p_key, r.query_arguments, expire_seconds, r.method)
            handler.set_status(status_code)
            if status_code != 200:
                log_func(message)
                return
            fn(*args, **kwargs)

        return wrapper

    return decorator


def signed(key_func, expire_seconds=10):
    """Validates the signature of the request before invoking the handler.
    If the signature fails a 401 is returned, or 406 is the signature has expired.

    Logging is passed by default to stdout.
    """

    def decorator(fn):

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            signed_log(key_func, print, expire_seconds)

        return wrapper

    return decorator


class StatusHandler(RequestHandler):
    __doc__ = 'Handler that calls each status job in a worker pool, attempting to timeout.\n    The resulting durations/errors are written to the response\n    as JSON.\n\n    eg.\n\n    `{\n        "endpoints": [\n            { "endpoint": "Jenny\'s Database", "duration": 1.002556324005127 },\n            { "endpoint": "Hotmail", "duration": -1, "error": "route to host down" },\n        ]\n     }`\n    '

    def initialize(self, jobs_func):
        self._jobs = jobs_func

    def get(self):
        endpoints = []
        stats = {'endpoints': None}
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        for job, future in [(job, executor.submit(timeit, job[2], number=1)) for job in self._jobs()]:
            name, timeout, _ = job
            endpoint = {'endpoint': name}
            try:
                data = future.result(timeout=timeout)
                endpoint['duration'] = data
            except concurrent.futures.TimeoutError:
                endpoint['error'] = 'timeout exceeded'
            except Exception as ex:
                endpoint['error'] = str(ex)

            endpoints.append(endpoint)

        if len(endpoints) > 0:
            stats['endpoints'] = endpoints
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(stats))
        executor.shutdown(wait=False)


class PingHandler(RequestHandler):
    __doc__ = 'Handler that simply returns `pong` from a GET.\n    '

    def get(self):
        self.write('pong')


class TimeHandler(RequestHandler):
    __doc__ = 'Handler that returns the systems current Epoch time.\n    '

    def get(self):
        utcnow = time.time()
        now_string = str(int(time.time()))
        self.write(now_string)