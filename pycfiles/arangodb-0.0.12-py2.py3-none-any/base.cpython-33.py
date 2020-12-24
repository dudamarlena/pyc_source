# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/clients/base.py
# Compiled at: 2013-12-06 03:31:22
# Size of source mod 2**32: 930 bytes
__all__ = ('RequestsBase', )

class RequestsBase(object):
    """RequestsBase"""

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