# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/weatherapi25/configuration25.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 3448 bytes
from pyowm.caches import nullcache
from pyowm.weatherapi25 import weathercoderegistry, cityidregistry
from pyowm.weatherapi25.parsers import forecastparser, observationlistparser, observationparser, stationhistoryparser, stationlistparser, stationparser, weatherhistoryparser
from pyowm.uvindexapi30.parsers import UVIndexParser, UVIndexListParser
from pyowm.pollutionapi30.parsers import COIndexParser, NO2IndexParser, SO2IndexParser, OzoneParser
API_SUBSCRIPTION_SUBDOMAINS = {'free': 'api', 
 'pro': 'pro'}
USE_SSL = False
VERIFY_SSL_CERTS = True
ROOT_API_URL = 'http://%s.openweathermap.org/data/2.5'
ROOT_HISTORY_URL = 'http://history.openweathermap.org/data/2.5'
OBSERVATION_URL = ROOT_API_URL + '/weather'
GROUP_OBSERVATIONS_URL = ROOT_API_URL + '/group'
STATION_URL = ROOT_API_URL + '/station'
FIND_OBSERVATIONS_URL = ROOT_API_URL + '/find'
FIND_STATION_URL = ROOT_API_URL + '/station/find'
BBOX_STATION_URL = ROOT_API_URL + '/box/station'
BBOX_CITY_URL = ROOT_API_URL + '/box/city'
THREE_HOURS_FORECAST_URL = ROOT_API_URL + '/forecast'
DAILY_FORECAST_URL = ROOT_API_URL + '/forecast/daily'
CITY_WEATHER_HISTORY_URL = ROOT_HISTORY_URL + '/history/city'
STATION_WEATHER_HISTORY_URL = ROOT_API_URL + '/history/station'
parsers = {'observation': observationparser.ObservationParser(), 
 'observation_list': observationlistparser.ObservationListParser(), 
 'forecast': forecastparser.ForecastParser(), 
 'weather_history': weatherhistoryparser.WeatherHistoryParser(), 
 'station_history': stationhistoryparser.StationHistoryParser(), 
 'station': stationparser.StationParser(), 
 'station_list': stationlistparser.StationListParser(), 
 'uvindex': UVIndexParser(), 
 'uvindex_list': UVIndexListParser(), 
 'coindex': COIndexParser(), 
 'ozone': OzoneParser(), 
 'no2index': NO2IndexParser(), 
 'so2index': SO2IndexParser()}
city_id_registry = cityidregistry.CityIDRegistry('cityids/%03d-%03d.txt.gz')
cache = nullcache.NullCache()
language = 'en'
API_SUBSCRIPTION_TYPE = 'free'
API_AVAILABILITY_TIMEOUT = 2
weather_code_registry = weathercoderegistry.WeatherCodeRegistry({'rain': [
          {'start': 500, 
           'end': 531},
          {'start': 300, 
           'end': 321}], 
 'sun': [
         {'start': 800, 
          'end': 800}], 
 'clouds': [
            {'start': 801, 
             'end': 804}], 
 'fog': [
         {'start': 741, 
          'end': 741}], 
 'haze': [
          {'start': 721, 
           'end': 721}], 
 'mist': [
          {'start': 701, 
           'end': 701}], 
 'snow': [
          {'start': 600, 
           'end': 622}], 
 'tornado': [
             {'start': 781, 
              'end': 781},
             {'start': 900, 
              'end': 900}], 
 'storm': [
           {'start': 901, 
            'end': 901},
           {'start': 960, 
            'end': 961}], 
 'hurricane': [
               {'start': 902, 
                'end': 902},
               {'start': 962, 
                'end': 962}]})