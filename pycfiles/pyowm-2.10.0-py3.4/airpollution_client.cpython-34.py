# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/pollutionapi30/airpollution_client.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 5441 bytes
from pyowm.utils import timeformatutils
from pyowm.pollutionapi30.uris import CO_INDEX_URL, OZONE_URL, NO2_INDEX_URL, SO2_INDEX_URL
from pyowm.commons import http_client

class AirPollutionHttpClient(object):
    __doc__ = '\n    A class representing the OWM Air Pollution web API, which is a subset of the\n    overall OWM API.\n\n    :param API_key: a Unicode object representing the OWM Air Pollution web API key\n    :type API_key: Unicode\n    :param httpclient: an *httpclient.HttpClient* instance that will be used to          send requests to the OWM Air Pollution web API.\n    :type httpclient: an *httpclient.HttpClient* instance\n\n    '

    def __init__(self, API_key, httpclient):
        self._API_key = API_key
        self._client = httpclient

    def _trim_to(self, date_object, interval):
        if interval == 'minute':
            return date_object.strftime('%Y-%m-%dT%H:%MZ')
        if interval == 'hour':
            return date_object.strftime('%Y-%m-%dT%HZ')
        if interval == 'day':
            return date_object.strftime('%Y-%m-%dZ')
        if interval == 'month':
            return date_object.strftime('%Y-%mZ')
        if interval == 'year':
            return date_object.strftime('%YZ')
        raise ValueError('The interval provided for the search window is invalid')

    def get_coi(self, params_dict):
        """
        Invokes the CO Index endpoint

        :param params_dict: dict of parameters
        :returns: a string containing raw JSON data
        :raises: *ValueError*, *APICallError*

        """
        lat = str(params_dict['lat'])
        lon = str(params_dict['lon'])
        start = params_dict['start']
        interval = params_dict['interval']
        if start is None:
            timeref = 'current'
        else:
            if interval is None:
                timeref = self._trim_to(timeformatutils.to_date(start), 'year')
            else:
                timeref = self._trim_to(timeformatutils.to_date(start), interval)
        fixed_url = '%s/%s,%s/%s.json' % (CO_INDEX_URL, lat, lon, timeref)
        uri = http_client.HttpClient.to_url(fixed_url, self._API_key, None)
        _, json_data = self._client.cacheable_get_json(uri)
        return json_data

    def get_o3(self, params_dict):
        """
        Invokes the O3 Index endpoint

        :param params_dict: dict of parameters
        :returns: a string containing raw JSON data
        :raises: *ValueError*, *APICallError*

        """
        lat = str(params_dict['lat'])
        lon = str(params_dict['lon'])
        start = params_dict['start']
        interval = params_dict['interval']
        if start is None:
            timeref = 'current'
        else:
            if interval is None:
                timeref = self._trim_to(timeformatutils.to_date(start), 'year')
            else:
                timeref = self._trim_to(timeformatutils.to_date(start), interval)
        fixed_url = '%s/%s,%s/%s.json' % (OZONE_URL, lat, lon, timeref)
        uri = http_client.HttpClient.to_url(fixed_url, self._API_key, None)
        _, json_data = self._client.cacheable_get_json(uri)
        return json_data

    def get_no2(self, params_dict):
        """
        Invokes the NO2 Index endpoint

        :param params_dict: dict of parameters
        :returns: a string containing raw JSON data
        :raises: *ValueError*, *APICallError*

        """
        lat = str(params_dict['lat'])
        lon = str(params_dict['lon'])
        start = params_dict['start']
        interval = params_dict['interval']
        if start is None:
            timeref = 'current'
        else:
            if interval is None:
                timeref = self._trim_to(timeformatutils.to_date(start), 'year')
            else:
                timeref = self._trim_to(timeformatutils.to_date(start), interval)
        fixed_url = '%s/%s,%s/%s.json' % (NO2_INDEX_URL, lat, lon, timeref)
        uri = http_client.HttpClient.to_url(fixed_url, self._API_key, None)
        _, json_data = self._client.cacheable_get_json(uri)
        return json_data

    def get_so2(self, params_dict):
        """
        Invokes the SO2 Index endpoint

        :param params_dict: dict of parameters
        :returns: a string containing raw JSON data
        :raises: *ValueError*, *APICallError*

        """
        lat = str(params_dict['lat'])
        lon = str(params_dict['lon'])
        start = params_dict['start']
        interval = params_dict['interval']
        if start is None:
            timeref = 'current'
        else:
            if interval is None:
                timeref = self._trim_to(timeformatutils.to_date(start), 'year')
            else:
                timeref = self._trim_to(timeformatutils.to_date(start), interval)
        fixed_url = '%s/%s,%s/%s.json' % (SO2_INDEX_URL, lat, lon, timeref)
        uri = http_client.HttpClient.to_url(fixed_url, self._API_key, None)
        _, json_data = self._client.cacheable_get_json(uri)
        return json_data

    def __repr__(self):
        return '<%s.%s - httpclient=%s>' % (
         __name__, self.__class__.__name__, str(self._client))