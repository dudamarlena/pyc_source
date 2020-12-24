# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmotd/__init__.py
# Compiled at: 2019-02-03 11:52:32
# Size of source mod 2**32: 452 bytes
from requests import get
import json

class DMOTD(object):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def raw(self):
        response = get(self.endpoint + '/raw')
        return response.text

    def json(self):
        response = get(self.endpoint + '/json')
        return response.json()