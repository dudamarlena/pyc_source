# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """StatusHandler"""

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
    """PingHandler"""

    def get(self):
        self.write('pong')


class TimeHandler(RequestHandler):
    """TimeHandler"""

    def get(self):
        utcnow = time.time()
        now_string = str(int(time.time()))
        self.write(now_string)