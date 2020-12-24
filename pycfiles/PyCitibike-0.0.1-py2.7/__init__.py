# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/pycitibike/__init__.py
# Compiled at: 2013-07-21 12:05:12
import requests

class Citibike(object):
    """
    A tiny API client for the citibike API
    """

    def __init__(self, host='appservices.citibikenyc.com'):
        self.host = host

    def stations(self, **kwargs):
        """
        Request a full list of stations for citibike

        :param kwargs: a dict of key values for the API.
            I'm actually not fully sure what this supports yet
        """
        return self._get('data2/stations', kwargs)

    def helmets(self, **kwargs):
        """
        Request a full list of places for helmets for citibike
        
        :param kwargs: a dict of key values for the API.
            I'm actually not fully sure what this supports yet
        """
        return self._get('v1/helmet/list', kwargs)

    def branches(self, **kwargs):
        """
        Request a full list of branches for citibike
        
        :param kwargs: a dict of key values for the API.
            I'm actually not fully sure what this supports yet
        """
        return self._get('v1/branch/list', kwargs)

    def _get(self, uri, options):
        """
        Quick and dirty wrapper around the requests object to do
        some simple data catching

        :params uri: a string, the uri you want to request
        :params options: a dict, the list of parameters you want to use
        """
        url = 'http://%s/%s' % (self.host, uri)
        r = requests.get(url, params=options)
        if r.status_code == 200:
            data = r.json()
            return data['results']
        r.raise_for_status()