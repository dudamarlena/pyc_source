# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/stationsapi30/aggregated_measurement_parser.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2221 bytes
__doc__ = '\nModule containing a concrete implementation for JSONParser abstract class,\nreturning an AggregatedMeasurement instance\n'
import json
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error
from pyowm.stationsapi30.measurement import AggregatedMeasurement

class AggregatedMeasurementParser(jsonparser.JSONParser):
    """AggregatedMeasurementParser"""

    def __init__(self):
        pass

    def parse_dict(self, data_dict):
        """
        Parses a dictionary representing the attributes of a
        *pyowm.stationsapi30.smeasurement.AggregatedMeasurement* entity
        :param data_dict: dict
        :return: *pyowm.stationsapi30.measurement.AggregatedMeasurement*
        """
        assert isinstance(data_dict, dict)
        string_repr = json.dumps(data_dict)
        return self.parse_JSON(string_repr)

    def parse_JSON(self, JSON_string):
        """
        Parses a *pyowm.stationsapi30.measurement.AggregatedMeasurement*
        instance out of raw JSON data.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :return: a *pyowm.stationsapi30.measurement.AggregatedMeasurement*
          instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        station_id = d.get('station_id', None)
        ts = d.get('date', None)
        if ts is not None:
            ts = int(ts)
        aggregated_on = d.get('type', None)
        temp = d.get('temp', dict())
        humidity = d.get('humidity', dict())
        wind = d.get('wind', dict())
        pressure = d.get('pressure', dict())
        precipitation = d.get('precipitation', dict())
        return AggregatedMeasurement(station_id, ts, aggregated_on, temp=temp, humidity=humidity, wind=wind, pressure=pressure, precipitation=precipitation)