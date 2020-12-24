# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /volume/flask_restpoints/handlers.py
# Compiled at: 2015-08-11 13:41:18
# Size of source mod 2**32: 2246 bytes
import concurrent.futures
from time import time
from timeit import timeit
from flask import jsonify

def status(jobs):
    """Handler that calls each status job in a worker pool, attempting to timeout.
    The resulting durations/errors are written to the response
    as JSON.

    eg.

    `{
        "endpoints": [
            { "endpoint": "Jenny's Database", "duration": 1.002556324005127 },
            { "endpoint": "Hotmail", "duration": -1, "error": "Host is down" },
        ]
     }`
    """

    def status_handler():
        endpoints = []
        stats = {'endpoints': None}
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        for job, future in [(job, executor.submit(timeit, job[2], number=1)) for job in jobs]:
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
        executor.shutdown(wait=False)
        return jsonify(**stats)

    return status_handler


def ping():
    """Handler that simply returns `pong` from a GET.
    """
    return 'pong'


def epoch():
    """Handler that returns the systems current Epoch time.
    """
    seconds = int(time())
    return str(seconds)