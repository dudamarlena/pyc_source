# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/weatherapi25/parsers/stationhistoryparser.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 4301 bytes
__doc__ = '\nModule containing a concrete implementation for JSONParser abstract class,\nreturning a StationHistory instance\n'
import json, time
from pyowm.weatherapi25 import stationhistory
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error, api_response_error

class StationHistoryParser(jsonparser.JSONParser):
    """StationHistoryParser"""

    def __init__(self):
        pass

    def parse_JSON(self, JSON_string):
        """
        Parses a *StationHistory* instance out of raw JSON data. Only certain
        properties of the data are used: if these properties are not found or
        cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: a *StationHistory* instance or ``None`` if no data is
            available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the JSON
            string embeds an HTTP status error

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        measurements = {}
        try:
            if 'cod' in d:
                if d['cod'] != '200':
                    raise api_response_error.APIResponseError('OWM API: error - response payload: ' + str(d), d['cod'])
            if str(d['cnt']) == '0':
                return
            for item in d['list']:
                if 'temp' not in item:
                    temp = None
                else:
                    if isinstance(item['temp'], dict):
                        temp = item['temp']['v']
                    else:
                        temp = item['temp']
                    if 'humidity' not in item:
                        hum = None
                    else:
                        if isinstance(item['humidity'], dict):
                            hum = item['humidity']['v']
                        else:
                            hum = item['humidity']
                        if 'pressure' not in item:
                            pres = None
                        else:
                            if isinstance(item['pressure'], dict):
                                pres = item['pressure']['v']
                            else:
                                pres = item['pressure']
                        if 'rain' in item and isinstance(item['rain']['today'], dict):
                            rain = item['rain']['today']['v']
                        else:
                            rain = None
                    if 'wind' in item and isinstance(item['wind']['speed'], dict):
                        wind = item['wind']['speed']['v']
                    else:
                        wind = None
                measurements[item['dt']] = {'temperature': temp,  'humidity': hum, 
                 'pressure': pres, 
                 'rain': rain, 
                 'wind': wind}

        except KeyError:
            raise parse_response_error.ParseResponseError(__name__ + ': impossible to read JSON data')

        current_time = round(time.time())
        return stationhistory.StationHistory(None, None, current_time, measurements)

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)