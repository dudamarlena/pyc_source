# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/auth.py
# Compiled at: 2018-07-26 12:24:59
# Size of source mod 2**32: 769 bytes
from carto.auth import _BaseUrlChecker
from carto.exceptions import CartoException
from pyrestcli.auth import BaseAuthClient

class LocationsCartoNoAuthClient(_BaseUrlChecker, BaseAuthClient):
    __doc__ = '\n    Simple Carto Auth class, without the API key in the request\n    '

    def __init__(self, base_url):
        base_url = self.check_base_url(base_url)
        super(LocationsCartoNoAuthClient, self).__init__(base_url)

    def send(self, relative_path, http_method, **requests_args):
        try:
            return (super(LocationsCartoNoAuthClient, self).send)(
             relative_path, 
             (http_method.lower()), **requests_args)
        except Exception as e:
            raise CartoException(e)