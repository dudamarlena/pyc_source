# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sci_api_req/providers/NASA/apod_provider.py
# Compiled at: 2019-08-28 08:55:31
# Size of source mod 2**32: 696 bytes
from datetime import date
from sci_api_req import config
from ..api_provider import ApiProvider

class APODProvider(ApiProvider):
    __doc__ = '\n    Astronomy picture of the day. Requires NASA api key.\n    For more informations see https://api.nasa.gov/api.html#apod\n    '

    def __init__(self):
        super(ApiProvider).__init__()
        self._api_url = 'https://api.nasa.gov/planetary/apod'

    @property
    def api_key(self) -> str:
        return config.get_api_keys('NASA')

    def get_apod(self, date=date.today(), hd=False):

        @self._get_request(('api_key={}'.format(self.api_key)), date=date, hd=hd)
        def inner(response):
            return response

        return inner