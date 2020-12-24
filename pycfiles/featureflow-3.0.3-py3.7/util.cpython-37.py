# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/featureflow/util.py
# Compiled at: 2019-03-01 22:03:23
# Size of source mod 2**32: 874 bytes
import time
from collections import OrderedDict
import requests

def chunked(f, chunksize=4096):
    data = f.read(chunksize)
    while data:
        yield data
        data = f.read(chunksize)


def dictify(x, key_selector=lambda item: id(item)):
    if x is None:
        return OrderedDict()
    if isinstance(x, dict):
        return x
    try:
        return OrderedDict(((key_selector(z), z) for z in x))
    except TypeError:
        return OrderedDict({key_selector(x): x})


def wait_for_http_server(host, port, wait_time_seconds=0.1, max_tries=100):
    for _ in range(max_tries):
        try:
            resp = requests.get(f"http://{host}:{port}")
            return resp
        except requests.exceptions.ConnectionError:
            time.sleep(wait_time_seconds)
            continue

    raise RuntimeError(f"Failed to start HTTP server at {host}:{port}")