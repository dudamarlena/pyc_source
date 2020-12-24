# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/stationsapi30/station_parser.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2157 bytes
__doc__ = '\nModule containing a concrete implementation for JSONParser abstract class,\nreturning a Station instance\n'
import json
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error
from pyowm.stationsapi30.station import Station

class StationParser(jsonparser.JSONParser):
    """StationParser"""

    def __init__(self):
        pass

    def parse_dict(self, data_dict):
        """
        Parses a dictionary representing the attributes of a
        *pyowm.stationsapi30.station.Station* entity
        :param data_dict: dict
        :return: *pyowm.stationsapi30.station.Station*
        """
        assert isinstance(data_dict, dict)
        string_repr = json.dumps(data_dict)
        return self.parse_JSON(string_repr)

    def parse_JSON(self, JSON_string):
        """
        Parses a *pyowm.stationsapi30.station.Station* instance out of raw JSON
        data.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :return: a *pyowm.stationsapi30.station.Station** instance or ``None``
            if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        try:
            id = d.get('ID', None) or d.get('id', None)
            external_id = d.get('external_id', None)
            lon = d.get('longitude', None)
            lat = d.get('latitude', None)
            alt = d.get('altitude', None)
        except KeyError as e:
            raise parse_response_error.ParseResponseError('Impossible to parse JSON: %s' % e)

        name = d.get('name', None)
        rank = d.get('rank', None)
        created_at = d.get('created_at', None)
        updated_at = d.get('updated_at', None)
        return Station(id, created_at, updated_at, external_id, name, lon, lat, alt, rank)