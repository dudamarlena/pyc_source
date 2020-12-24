# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tests/mocks/__init__.py
# Compiled at: 2019-10-31 01:58:57
# Size of source mod 2**32: 401 bytes
import requests

class MultiEndpointRequest(object):
    """MultiEndpointRequest"""

    def __init__(self, dict):
        self.dict = dict

    def get(self, url):
        try:
            return self.dict[url]
        except KeyError:
            raise requests.exceptions.ConnectionError