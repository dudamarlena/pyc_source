# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/weatherapi25/parsers/stationlistparser.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 1407 bytes
"""
Module containing a concrete implementation for JSONParser abstract class,
returning a list of Station instances
"""
import json
from pyowm.abstractions.jsonparser import JSONParser
from pyowm.weatherapi25.parsers.stationparser import StationParser
from pyowm.exceptions.parse_response_error import ParseResponseError

class StationListParser(JSONParser):
    __doc__ = '\n    Concrete *JSONParser* implementation building a list of *Station*\n    instances out of raw JSON data coming from OWM Weather API responses.\n\n    '

    def parse_JSON(self, JSON_string):
        """
        Parses a list of *Station* instances out of raw JSON data. Only
        certain properties of the data are used: if these properties are not
        found or cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: a list of *Station* instances or ``None`` if no data is
            available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the OWM API
            returns a HTTP status error

        """
        if JSON_string is None:
            raise ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        station_parser = StationParser()
        return [station_parser.parse_JSON(json.dumps(item)) for item in d]