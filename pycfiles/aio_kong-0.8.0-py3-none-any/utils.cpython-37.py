# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/kong/utils.py
# Compiled at: 2019-08-12 17:48:16
# Size of source mod 2**32: 764 bytes
import socket
from uuid import UUID
from multidict import MultiDict

def as_list(key, data):
    v = data.get(key)
    if isinstance(v, str):
        v = [
         v]
    elif not isinstance(v, list):
        v = []
    data[key] = v
    return data


def as_dict(data, key='data'):
    if not isinstance(data, dict):
        return {key: data}
    return data


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    try:
        return s.getsockname()[0]
    finally:
        s.close()


def as_params(*, params=None, **kwargs):
    params = MultiDict(params if params is not None else {})
    params.update(kwargs)
    return params


def uid(id_):
    try:
        return str(UUID(id_))
    except ValueError:
        return id_