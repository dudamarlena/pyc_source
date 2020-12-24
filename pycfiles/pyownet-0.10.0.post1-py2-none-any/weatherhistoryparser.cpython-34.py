# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/weatherapi25/parsers/weatherhistoryparser.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2937 bytes
__doc__ = '\nModule containing a concrete implementation for JSONParser abstract class,\nreturning a list of Weather objects\n'
import json
from pyowm.weatherapi25 import weather
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error, api_response_error

class WeatherHistoryParser(jsonparser.JSONParser):
    """WeatherHistoryParser"""

    def __init__(self):
        pass

    def parse_JSON(self, JSON_string):
        """
        Parses a list of *Weather* instances out of raw JSON data. Only certain
        properties of the data are used: if these properties are not found or
        cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: a list of *Weather* instances or ``None`` if no data is
            available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the JSON
            string embeds an HTTP status error

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        if 'message' in d and 'cod' in d:
            if d['cod'] == '404':
                print('OWM API: data not found - response payload: ' + json.dumps(d))
                return
            if d['cod'] != '200':
                raise api_response_error.APIResponseError('OWM API: error - response payload: ' + json.dumps(d), d['cod'])
            if 'cnt' in d and d['cnt'] == '0':
                return []
            if 'list' in d:
                pass
            try:
                return [weather.weather_from_dictionary(item) for item in d['list']]
            except KeyError:
                raise parse_response_error.ParseResponseError(''.join([__name__, ': impossible to read weather info from JSON data']))

        else:
            raise parse_response_error.ParseResponseError(''.join([__name__, ': impossible to read weather list from JSON data']))

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)