# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/weatherapi25/parsers/stationparser.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2381 bytes
"""
Module containing a concrete implementation for JSONParser abstract class,
returning a Station instance
"""
import json, time
from pyowm.weatherapi25 import station
from pyowm.weatherapi25 import weather
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error, api_response_error

class StationParser(jsonparser.JSONParser):
    __doc__ = '\n    Concrete *JSONParser* implementation building a *Station* instance\n    out of raw JSON data coming from OWM Weather API responses.\n\n    '

    def parse_JSON(self, JSON_string):
        """
        Parses a *Station* instance out of raw JSON data. Only certain
        properties of the data are used: if these properties are not found or
        cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: a *Station* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the JSON
            string embeds an HTTP status error

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        try:
            name = d['station']['name']
            station_ID = d['station']['id']
            station_type = d['station']['type']
            status = d['station']['status']
            lat = d['station']['coord']['lat']
            if 'lon' in d['station']['coord']:
                lon = d['station']['coord']['lon']
            else:
                if 'lng' in d['station']['coord']:
                    lon = d['station']['coord']['lng']
                else:
                    lon = None
                if 'distance' in d:
                    distance = d['distance']
                else:
                    distance = None
        except KeyError as e:
            error_msg = ''.join((__name__, ': unable to read JSON data'))
            raise parse_response_error.ParseResponseError(error_msg)
        else:
            if 'last' in d:
                last_weather = weather.weather_from_dictionary(d['last'])
            else:
                last_weather = None
            return station.Station(name, station_ID, station_type, status, lat, lon, distance, last_weather)