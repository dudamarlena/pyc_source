# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tests/mocks/__init__.py
# Compiled at: 2019-10-31 01:58:57
# Size of source mod 2**32: 401 bytes
import requests

class MultiEndpointRequest(object):
    __doc__ = " A requests.get mock that returns different results for different endpoints and raises ConnectionError if\n    the endpoint isn't set"

    def __init__(self, dict):
        self.dict = dict

    def get(self, url):
        try:
            return self.dict[url]
        except KeyError:
            raise requests.exceptions.ConnectionError