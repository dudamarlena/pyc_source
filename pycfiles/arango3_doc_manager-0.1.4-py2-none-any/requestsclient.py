# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/clients/requestsclient.py
# Compiled at: 2013-02-24 07:44:12
import logging
try:
    import requests
except ImportError:
    raise ImportError('Please, install ``requests`` library to use this client')

from .base import RequestsBase
__all__ = ('RequestsClient', )
logger = logging.getLogger('arango.requests')
sess = requests.Session()

class RequestsClient(RequestsBase):
    """
    If no PyCURL bindings available or
    client forced by hands. Quite useful for PyPy.
    """
    _config = {}

    @classmethod
    def config(cls, **kwargs):
        cls._config.update(kwargs)

    @classmethod
    def get(cls, url, **kwargs):
        r = sess.get(url, **cls._config)
        return cls.build_response(r.status_code, r.reason, r.headers, r.text)

    @classmethod
    def post(cls, url, data=None):
        if data is None:
            data = ''
        r = sess.post(url, data=data, **cls._config)
        return cls.build_response(r.status_code, r.reason, r.headers, r.text)

    @classmethod
    def put(cls, url, data=None):
        if data is None:
            data = ''
        r = sess.put(url, data=data, **cls._config)
        return cls.build_response(r.status_code, r.reason, r.headers, r.text)

    @classmethod
    def delete(cls, url, data=None):
        r = sess.delete(url, **cls._config)
        return cls.build_response(r.status_code, r.reason, r.headers, r.text)