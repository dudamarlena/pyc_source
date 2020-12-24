# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stanley/PycharmProjects/horizon-python-client/src/mf_horizon_client/client/error.py
# Compiled at: 2020-03-26 22:31:55
# Size of source mod 2**32: 505 bytes
from requests import Response

class HorizonError(RuntimeError):
    __doc__ = 'Wrapper class for an error :class:`.Response` received from Horizon.'

    def __init__(self, response):
        self.status_code = response.status_code
        try:
            self.message = response.json()['message']
        except BaseException:
            self.message = response.content.decode() if response.content else ''

        super().__init__(f"Status: {self.status_code}  Message: {self.message}")