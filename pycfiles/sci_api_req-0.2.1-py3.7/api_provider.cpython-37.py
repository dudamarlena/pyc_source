# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sci_api_req/providers/api_provider.py
# Compiled at: 2019-08-29 14:56:18
# Size of source mod 2**32: 941 bytes
from functools import wraps
import requests

class ApiProvider(object):
    __doc__ = 'Parent class for api requesters'
    __slots__ = ['_api_url', '_api_key']

    def __init__(self):
        self._api_url = None
        self._api_key = None

    def _get_request(self, endpoint: str, **parameters):
        """Make GET request to api and inject response to response kwarg"""

        def inner_function(f):

            @wraps(f)
            def wrapper():
                if self._api_key:
                    parameters['api_key'] = self._api_key
                else:
                    response = requests.get((self._api_url + endpoint), params=parameters)
                    if response.content:
                        response = response.json()
                    else:
                        print('WARNING!!! Api returned empty response. That could cause exception')
                return f(response=response)

            return wrapper()

        return inner_function