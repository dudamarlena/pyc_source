# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/utils/http_verifier.py
# Compiled at: 2015-03-27 17:46:10
# Size of source mod 2**32: 844 bytes
import time, requests
from requests import exceptions as reqexcept
from .verifier import Verifier

class HttpOkVerifier(Verifier):

    def __init__(self, **kwargs):
        self.url = ''
        self.timeout = 30
        self.interval = 1
        self.headers = {}
        if 'url' in kwargs:
            self.url = kwargs['url']
        if 'timeout' in kwargs:
            self.timeout = kwars['timeout']
        if 'interval' in kwargs:
            self.interval = kwargs['interval']
        if 'headers' in kwargs:
            self.headers = kwargs['headers']

    def run(self, proc):
        passed = False
        timeout_at = time.time() + self.timeout
        while not passed and time.time() < timeout_at:
            try:
                resp = requests.get(self.url, headers=self.headers, timeout=self.interval)
                if resp.status_code >= 200:
                    if resp.status_code < 300:
                        passed = True
            except reqexcept.ConnectionError:
                pass

        return passed