# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/weatherapi25/parsers/observationparser.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2893 bytes
__doc__ = '\nModule containing a concrete implementation for JSONParser abstract class,\nreturning Observation objects\n'
from json import loads, dumps
from time import time
from pyowm.weatherapi25 import observation
from pyowm.weatherapi25 import location
from pyowm.weatherapi25 import weather
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error, api_response_error

class ObservationParser(jsonparser.JSONParser):
    """ObservationParser"""

    def __init__(self):
        pass

    def parse_JSON(self, JSON_string):
        """
        Parses an *Observation* instance out of raw JSON data. Only certain
        properties of the data are used: if these properties are not found or
        cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: an *Observation* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the JSON
            string embeds an HTTP status error

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = loads(JSON_string)
        if 'message' in d and 'cod' in d:
            if d['cod'] == '404':
                print('OWM API: observation data not available - response payload: ' + dumps(d))
                return
            raise api_response_error.APIResponseError('OWM API: error - response payload: ' + dumps(d), d['cod'])
        try:
            place = location.location_from_dictionary(d)
        except KeyError:
            raise parse_response_error.ParseResponseError(''.join([__name__, ': impossible to read location info from JSON data']))

        try:
            w = weather.weather_from_dictionary(d)
        except KeyError:
            raise parse_response_error.ParseResponseError(''.join([__name__, ': impossible to read weather info from JSON data']))

        current_time = int(round(time()))
        return observation.Observation(current_time, place, w)

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)