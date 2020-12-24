# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/uvindexapi30/parsers.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 3349 bytes
"""
Module containing a concrete implementation for JSONParser abstract class,
returning UVIndex objects
"""
import json
from pyowm.uvindexapi30 import uvindex
from pyowm.weatherapi25 import location
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error
from pyowm.utils import timeutils

class UVIndexParser(jsonparser.JSONParser):
    __doc__ = '\n    Concrete *JSONParser* implementation building an *UVIndex* instance out\n    of raw JSON data coming from OWM Weather API responses.\n\n    '

    def __init__(self):
        pass

    def parse_JSON(self, JSON_string):
        """
        Parses an *UVIndex* instance out of raw JSON data. Only certain
        properties of the data are used: if these properties are not found or
        cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: an *UVIndex* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the JSON
            string embeds an HTTP status error

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        try:
            reference_time = d['date']
            reception_time = timeutils.now('unix')
            lon = float(d['lon'])
            lat = float(d['lat'])
            place = location.Location(None, lon, lat, None)
            uv_intensity = float(d['value'])
        except KeyError:
            raise parse_response_error.ParseResponseError(''.join([__name__, ': impossible to parse UV Index']))

        return uvindex.UVIndex(reference_time, place, uv_intensity, reception_time)

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)


class UVIndexListParser(jsonparser.JSONParser):
    __doc__ = '\n    Concrete *JSONParser* implementation building a list of *UVIndex* instances\n    out of raw JSON data coming from OWM Weather API responses.\n\n    '

    def __init__(self):
        pass

    def parse_JSON(self, JSON_string):
        """
        Parses a list of *UVIndex* instances out of raw JSON data. Only certain
        properties of the data are used: if these properties are not found or
        cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: a list of *UVIndex* instances or an empty list if no data is
            available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the JSON
            string embeds an HTTP status error

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        uvindex_parser = UVIndexParser()
        return [uvindex_parser.parse_JSON(json.dumps(item)) for item in d]

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)