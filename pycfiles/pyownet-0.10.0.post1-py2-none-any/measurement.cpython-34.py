# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/stationsapi30/measurement.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 10580 bytes
import json
from pyowm.utils import timeformatutils

class AggregatedMeasurement:
    """AggregatedMeasurement"""
    ALLOWED_AGGREGATION_TIME_FRAMES = [
     'm', 'h', 'd']

    def __init__(self, station_id, timestamp, aggregated_on, temp=None, humidity=None, wind=None, pressure=None, precipitation=None):
        assert station_id is not None
        assert isinstance(timestamp, int)
        assert not timestamp < 0
        assert aggregated_on is not None
        if aggregated_on not in self.ALLOWED_AGGREGATION_TIME_FRAMES:
            raise ValueError('"aggregated_on" must be among: m, h, d')
        self.station_id = station_id
        self.timestamp = timestamp
        self.aggregated_on = aggregated_on
        self.temp = dict() if temp is None else temp
        self.humidity = dict() if humidity is None else humidity
        self.wind = dict() if wind is None else wind
        self.pressure = dict() if pressure is None else pressure
        self.precipitation = dict() if precipitation is None else precipitation

    def creation_time(self, timeformat='unix'):
        """Returns the UTC time of creation of this aggregated measurement

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time, '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00`` or `date` for
            a ``datetime.datetime`` object
        :type timeformat: str
        :returns: an int or a str or a ``datetime.datetime`` object or None
        :raises: ValueError

        """
        if self.timestamp is None:
            return
        return timeformatutils.timeformat(self.timestamp, timeformat)

    def to_dict(self):
        """Dumps object fields into a dict

        :returns: a dict

        """
        return {'station_id': self.station_id,  'timestamp': self.timestamp, 
         'aggregated_on': self.aggregated_on, 
         'temp': self.temp, 
         'humidity': self.humidity, 
         'wind': self.wind, 
         'pressure': self.pressure, 
         'precipitation': self.precipitation}

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns: the JSON string

        """
        return json.dumps(self.to_dict())

    def __repr__(self):
        return '<%s.%s - station_id=%s, created_at=%s>' % (
         __name__, self.__class__.__name__,
         self.station_id, self.creation_time())


class Measurement:

    def __init__(self, station_id, timestamp, temperature=None, wind_speed=None, wind_gust=None, wind_deg=None, pressure=None, humidity=None, rain_1h=None, rain_6h=None, rain_24h=None, snow_1h=None, snow_6h=None, snow_24h=None, dew_point=None, humidex=None, heat_index=None, visibility_distance=None, visibility_prefix=None, clouds_distance=None, clouds_condition=None, clouds_cumulus=None, weather_precipitation=None, weather_descriptor=None, weather_intensity=None, weather_proximity=None, weather_obscuration=None, weather_other=None):
        assert station_id is not None
        assert isinstance(timestamp, int)
        assert not timestamp < 0
        self.station_id = station_id
        self.timestamp = timestamp
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.wind_gust = wind_gust
        self.wind_deg = wind_deg
        self.pressure = pressure
        self.humidity = humidity
        self.rain_1h = rain_1h
        self.rain_6h = rain_6h
        self.rain_24h = rain_24h
        self.snow_1h = snow_1h
        self.snow_6h = snow_6h
        self.snow_24h = snow_24h
        self.dew_point = dew_point
        self.humidex = humidex
        self.heat_index = heat_index
        self.visibility_distance = visibility_distance
        self.visibility_prefix = visibility_prefix
        self.clouds_distance = clouds_distance
        self.clouds_condition = clouds_condition
        self.clouds_cumulus = clouds_cumulus
        self.weather_precipitation = weather_precipitation
        self.weather_descriptor = weather_descriptor
        self.weather_intensity = weather_intensity
        self.weather_proximity = weather_proximity
        self.weather_obscuration = weather_obscuration
        self.weather_other = weather_other

    def creation_time(self, timeformat='unix'):
        """Returns the UTC time of creation of this raw measurement

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time, '*iso*' for ISO8601-formatted
            string in the format ``YYYY-MM-DD HH:MM:SS+00`` or `date` for
            a ``datetime.datetime`` object
        :type timeformat: str
        :returns: an int or a str or a ``datetime.datetime`` object or None
        :raises: ValueError

        """
        if self.timestamp is None:
            return
        return timeformatutils.timeformat(self.timestamp, timeformat)

    @classmethod
    def from_dict(cls, the_dict):
        if 'station_id' not in the_dict:
            raise KeyError('"station_id" must be provided')
        station_id = the_dict['station_id']
        if 'timestamp' not in the_dict:
            raise KeyError('"timestamp" must be provided')
        timestamp = the_dict['timestamp']
        temperature = the_dict.get('temperature', None)
        wind_speed = the_dict.get('wind_speed', None)
        wind_gust = the_dict.get('wind_gust', None)
        wind_deg = the_dict.get('wind_deg', None)
        pressure = the_dict.get('pressure', None)
        humidity = the_dict.get('humidity', None)
        rain_1h = the_dict.get('rain_1h', None)
        rain_6h = the_dict.get('rain_6h', None)
        rain_24h = the_dict.get('rain_24h', None)
        snow_1h = the_dict.get('snow_1h', None)
        snow_6h = the_dict.get('snow_6h', None)
        snow_24h = the_dict.get('snow_24h', None)
        dew_point = the_dict.get('dew_point', None)
        humidex = the_dict.get('humidex', None)
        heat_index = the_dict.get('heat_index', None)
        visibility_distance = the_dict.get('visibility_distance', None)
        visibility_prefix = the_dict.get('visibility_prefix', None)
        clouds_distance = the_dict.get('clouds_distance', None)
        clouds_condition = the_dict.get('clouds_condition', None)
        clouds_cumulus = the_dict.get('clouds_cumulus', None)
        weather_precipitation = the_dict.get('weather_precipitation', None)
        weather_descriptor = the_dict.get('weather_descriptor', None)
        weather_intensity = the_dict.get('weather_intensity', None)
        weather_proximity = the_dict.get('weather_proximity', None)
        weather_obscuration = the_dict.get('weather_obscuration', None)
        weather_other = the_dict.get('weather_other', None)
        return Measurement(station_id, timestamp, temperature=temperature, wind_speed=wind_speed, wind_gust=wind_gust, wind_deg=wind_deg, pressure=pressure, humidity=humidity, rain_1h=rain_1h, rain_6h=rain_6h, rain_24h=rain_24h, snow_1h=snow_1h, snow_6h=snow_6h, snow_24h=snow_24h, dew_point=dew_point, humidex=humidex, heat_index=heat_index, visibility_distance=visibility_distance, visibility_prefix=visibility_prefix, clouds_distance=clouds_distance, clouds_condition=clouds_condition, clouds_cumulus=clouds_cumulus, weather_precipitation=weather_precipitation, weather_descriptor=weather_descriptor, weather_intensity=weather_intensity, weather_proximity=weather_proximity, weather_obscuration=weather_obscuration, weather_other=weather_other)

    def to_dict(self):
        """Dumps object fields into a dictionary

        :returns: a dict

        """
        return {'station_id': self.station_id, 
         'timestamp': self.timestamp, 
         'temperature': self.temperature, 
         'wind_speed': self.wind_speed, 
         'wind_gust': self.wind_gust, 
         'wind_deg': self.wind_deg, 
         'pressure': self.pressure, 
         'humidity': self.humidity, 
         'rain_1h': self.rain_1h, 
         'rain_6h': self.rain_6h, 
         'rain_24h': self.rain_24h, 
         'snow_1h': self.snow_1h, 
         'snow_6h': self.snow_6h, 
         'snow_24h': self.snow_24h, 
         'dew_point': self.dew_point, 
         'humidex': self.humidex, 
         'heat_index': self.heat_index, 
         'visibility_distance': self.visibility_distance, 
         'visibility_prefix': self.visibility_prefix, 
         'clouds_distance': self.clouds_distance, 
         'clouds_condition': self.clouds_condition, 
         'clouds_cumulus': self.clouds_cumulus, 
         'weather_precipitation': self.weather_precipitation, 
         'weather_descriptor': self.weather_descriptor, 
         'weather_intensity': self.weather_intensity, 
         'weather_proximity': self.weather_proximity, 
         'weather_obscuration': self.weather_obscuration, 
         'weather_other': self.weather_other}

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns: the JSON string

        """
        return json.dumps(self.to_dict())

    def __repr__(self):
        return '<%s.%s - station_id=%s, created_at=%s>' % (
         __name__, self.__class__.__name__,
         self.station_id, self.creation_time())