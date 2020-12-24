# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\config.py
# Compiled at: 2016-09-14 04:38:46
# Size of source mod 2**32: 2721 bytes
from distutils.util import strtobool
from datascryer.helper.python import python_3
if python_3():
    import configparser
else:
    import ConfigParser

class ConfigfileException(Exception):
    pass


class Config:
    data = dict()

    def __init__(self, file):
        if python_3():
            self._Config__settings = configparser.ConfigParser()
        else:
            self._Config__settings = ConfigParser.SafeConfigParser()
        try:
            with open(file) as (f):
                self._Config__settings.readfp(f)
        except IOError as e:
            raise ConfigfileException(e)

        self.data['main'] = {'customMethods': self._Config__settings.get('Main', 'Custom_Methods'), 
         'log_level': self._Config__settings.get('Main', 'Log_Level'), 
         'daemon': strtobool(self._Config__settings.get('Main', 'Daemon')), 
         'update_rate': int(self._Config__settings.get('Main', 'Config_Updaterate_in_Minutes')) * 60, 
         'log_performance': strtobool(self._Config__settings.get('Main', 'Log_Performance'))}
        livestatus_split = self._Config__settings.get('Livestatus', 'Address').split(':')
        self.data['livestatus'] = {'protocol': livestatus_split[0], 'address': livestatus_split[1]}
        if len(livestatus_split) == 3:
            self.data['livestatus']['port'] = int(livestatus_split[2])
        histou_split = self._Config__settings.get('Histou', 'Address').split(':', 1)
        self.data['histou'] = {'prot': histou_split[0], 'address': histou_split[1]}
        self.data['histou']['user'] = self._Config__settings.get('Histou', 'User')
        self.data['histou']['password'] = self._Config__settings.get('Histou', 'Password')
        self.data['influxdb'] = {'read': {'address': self._Config__settings.get('InfluxDB', 'Address_Read'), 
                  'db': self._Config__settings.get('InfluxDB', 'DB_Read'), 
                  'args': self._Config__settings.get('InfluxDB', 'DB_Read_Args')}, 
         
         'write': {'address': self._Config__settings.get('InfluxDB', 'Address_Write'), 
                   'db_forecast': self._Config__settings.get('InfluxDB', 'DB_Write_Forecast'), 
                   'db_anomaly': self._Config__settings.get('InfluxDB', 'DB_Write_Anomaly'), 
                   'args': self._Config__settings.get('InfluxDB', 'DB_Write_Args')}}


def log_peformance():
    return Config.data['main']['log_performance']