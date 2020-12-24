# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/uvindexapi30/uv_client.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 3493 bytes
from pyowm.uvindexapi30.uris import UV_INDEX_URL, UV_INDEX_FORECAST_URL, UV_INDEX_HISTORY_URL
from pyowm.commons import http_client

class UltraVioletHttpClient(object):
    __doc__ = '\n    An HTTP client class for the OWM UV web API, which is a subset of the\n    overall OWM API.\n\n    :param API_key: a Unicode object representing the OWM UV web API key\n    :type API_key: Unicode\n    :param httpclient: an *httpclient.HttpClient* instance that will be used to          send requests to the OWM Air Pollution web API.\n    :type httpclient: an *httpclient.HttpClient* instance\n\n    '

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
        raise ValueError('The interval provided for UVIndex search window is invalid')

    def get_uvi(self, params_dict):
        """
        Invokes the UV Index endpoint

        :param params_dict: dict of parameters
        :returns: a string containing raw JSON data
        :raises: *ValueError*, *APICallError*

        """
        lat = str(params_dict['lat'])
        lon = str(params_dict['lon'])
        params = dict(lat=lat, lon=lon)
        uri = http_client.HttpClient.to_url(UV_INDEX_URL, self._API_key, None)
        _, json_data = self._client.cacheable_get_json(uri, params=params)
        return json_data

    def get_uvi_forecast(self, params_dict):
        """
        Invokes the UV Index Forecast endpoint

        :param params_dict: dict of parameters
        :returns: a string containing raw JSON data
        :raises: *ValueError*, *APICallError*

        """
        lat = str(params_dict['lat'])
        lon = str(params_dict['lon'])
        params = dict(lat=lat, lon=lon)
        uri = http_client.HttpClient.to_url(UV_INDEX_FORECAST_URL, self._API_key, None)
        _, json_data = self._client.cacheable_get_json(uri, params=params)
        return json_data

    def get_uvi_history(self, params_dict):
        """
        Invokes the UV Index History endpoint

        :param params_dict: dict of parameters
        :returns: a string containing raw JSON data
        :raises: *ValueError*, *APICallError*

        """
        lat = str(params_dict['lat'])
        lon = str(params_dict['lon'])
        start = str(params_dict['start'])
        end = str(params_dict['end'])
        params = dict(lat=lat, lon=lon, start=start, end=end)
        uri = http_client.HttpClient.to_url(UV_INDEX_HISTORY_URL, self._API_key, None)
        _, json_data = self._client.cacheable_get_json(uri, params=params)
        return json_data

    def __repr__(self):
        return '<%s.%s - httpclient=%s>' % (
         __name__, self.__class__.__name__, str(self._client))