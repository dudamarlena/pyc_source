# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/toxiproxy/api.py
# Compiled at: 2019-01-23 10:28:28
# Size of source mod 2**32: 1652 bytes
import requests
from future.utils import raise_with_traceback
from .exceptions import ProxyExists, NotFound, InvalidToxic

class APIConsumer(object):
    __doc__ = ' Toxiproxy API Consumer '
    host = '127.0.0.1'
    port = 8474

    @classmethod
    def get(cls, url, params=None, **kwargs):
        """ Use the GET method to fetch data from the API """
        base_url = 'http://%s:%s' % (cls.host, cls.port)
        endpoint = base_url + url
        return validate_response((requests.get)(url=endpoint, params=params, **kwargs))

    @classmethod
    def delete(cls, url, **kwargs):
        """ Use the DELETE method to delete data from the API """
        base_url = 'http://%s:%s' % (cls.host, cls.port)
        endpoint = base_url + url
        return validate_response((requests.delete)(url=endpoint, **kwargs))

    @classmethod
    def post(cls, url, data=None, json=None, **kwargs):
        """ Use the POST method to post data to the API """
        base_url = 'http://%s:%s' % (cls.host, cls.port)
        endpoint = base_url + url
        return validate_response((requests.post)(url=endpoint, data=data, json=json, **kwargs))


def validate_response(response):
    """
    Handle the received response to make sure that we
    will only process valid requests.
    """
    content = response.content
    if response.status_code == 409:
        raise_with_traceback(ProxyExists(content))
    else:
        if response.status_code == 404:
            raise_with_traceback(NotFound(content))
        else:
            if response.status_code == 400:
                raise_with_traceback(InvalidToxic(content))
    return response