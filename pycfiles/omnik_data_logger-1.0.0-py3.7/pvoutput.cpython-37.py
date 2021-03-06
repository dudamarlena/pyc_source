# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/omnik/plugins/pvoutput.py
# Compiled at: 2020-01-12 07:08:27
# Size of source mod 2**32: 3598 bytes
import json
from datetime import datetime
import pytz, urllib.parse, requests
from omnik.plugins import Plugin

class pvoutput(Plugin):

    def __init__(self):
        super().__init__()
        self.name = 'pvoutput'
        self.description = 'Write output to PVOutput'
        tz = self.config.get('default', 'timezone', fallback='Europe/Amsterdam')
        self.timezone = pytz.timezone(tz)

    def get_weather(self):
        try:
            if 'weather' not in self.cache:
                self.logger.debug('[cache miss] Fetching weather data')
                url = 'https://{endpoint}/data/2.5/weather?lon={lon}&lat={lat}&units={units}&APPID={api_key}'.format(endpoint=(self.config.get('openweathermap', 'endpoint')),
                  lat=(self.config.get('openweathermap', 'lat')),
                  lon=(self.config.get('openweathermap', 'lon')),
                  units=self.config.get('openweathermap',
                  'units', fallback='metric'),
                  api_key=(self.config.get('openweathermap', 'api_key')))
                res = requests.get(url)
                res.raise_for_status()
                self.cache['weather'] = res.json()
            return self.cache['weather']
        except requests.exceptions.HTTPError as e:
            try:
                self.logger.error('Unable to get data. [{0}]: {1}'.format(type(e).__name__, str(e)))
                raise e
            finally:
                e = None
                del e

    def process(self, **args):
        """
        Send data to pvoutput
        """
        try:
            now = self.timezone.normalize(self.timezone.fromutc(datetime.utcnow()))
            msg = args['msg']
            self.logger.debug(json.dumps(msg, indent=2))
            self.config.has_option('pvoutput', 'sys_id') and self.config.has_option('pvoutput', 'api_key') or self.logger.error(f"[{__name__}] No api_key and/or sys_id found in configuration")
            return
            headers = {'X-Pvoutput-Apikey':self.config.get('pvoutput', 'api_key'), 
             'X-Pvoutput-SystemId':self.config.get('pvoutput', 'sys_id'), 
             'Content-type':'application/x-www-form-urlencoded', 
             'Accept':'text/plain'}
            data = {'d':now.strftime('%Y%m%d'), 
             't':now.strftime('%H:%M'), 
             'v1':str(float(msg['today_energy']) * 1000), 
             'v2':str(float(msg['current_power']) * 1000)}
            if self.config.getboolean('pvoutput', 'use_temperature', fallback=False):
                weather = self.get_weather()
                data['v5'] = str(weather['main']['temp'])
            encoded = urllib.parse.urlencode(data)
            self.logger.debug(json.dumps(data, indent=2))
            r = requests.post('http://pvoutput.org/service/r2/addstatus.jsp',
              data=encoded, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                if e.status_code == '400':
                    self.logger.warn(f"Got error from pvoutput: {str(e)} (ignoring: if this happens a lot ... fix it)")
                else:
                    if e.status_code == '504':
                        pass
            finally:
                e = None
                del e

        except Exception as e:
            try:
                self.logger.error(e, exc_info=True)
                raise e
            finally:
                e = None
                del e