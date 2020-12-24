# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/clients/base.py
# Compiled at: 2013-12-06 03:31:22
# Size of source mod 2**32: 930 bytes
__all__ = ('RequestsBase', )

class RequestsBase(object):
    __doc__ = '\n    Base class to implement HTTP client\n    '

    @classmethod
    def build_response(cls, status, message, headers, body):
        if str(type(body)) == "<class 'bytes'>":
            body = body.decode('utf-8')
        d = {'text': body, 
         'headers': headers, 
         'message': message, 
         'status_code': status}
        return type('ArangoHttpResponse', (object,), d)

    def get(*args, **kwargs):
        raise NotImplementedError

    def post(*args, **kwargs):
        raise NotImplementedError

    def put(*args, **kwargs):
        raise NotImplementedError

    def delete(*args, **kwargs):
        raise NotImplementedError

    def multipart(requests):
        """
        Method to collecto multiple requests and
        send it as a batch using **HttpBatch API**.
        """
        pass