# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/route_api/avishan/utils.py
# Compiled at: 2020-03-01 13:20:49
# Size of source mod 2**32: 1071 bytes
import datetime, decimal, falcon
from falcon.request import Request
from falcon.response import Response

class AvishanRequest:
    req = None
    req: Request
    data = {}
    data: dict
    params = {}
    params: dict

    def __init__(self, req: Request):
        self.req = req
        data = {}
        if 'request' in req.context.keys():
            data = req.context['request']
        self.data = data
        self.params = req.params


class AvishanResponse:
    res = None
    res: Response
    data = {}
    data: dict
    status_code = falcon.HTTP_200

    def __init__(self, res: Response, data: dict=None):
        if data is None:
            data = {}
        self.res = res
        self.data = data


def json_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return str(obj)
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError('Cannot serialize {!r} (type {})'.format(obj, type(obj)))


def all_subclasses(cls):
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])