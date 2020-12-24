# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\jobs\job.py
# Compiled at: 2016-09-14 07:54:42
# Size of source mod 2**32: 7390 bytes
import logging, math, threading, time
from random import randint
from datascryer.config import log_peformance
from datascryer.helper.python import python_3, delta_ms
from datascryer.helper.time_converter import string_to_ms
from datascryer.influxdb.reader import InfluxDBReader
from datascryer.influxdb.writer import InfluxDBWriter
from datascryer.methods.method_collector import MethodCollector
if python_3():
    from urllib.error import URLError
else:
    from urllib2 import URLError
METHOD = 'method'
LABEL = 'label'
UPDATE_RATE = 'update_rate'
LOOKBACK_RANGE = 'lookback_range'
FORECAST_RANGE = 'forecast_range'
FORECAST_INTERVAL = 'forecast_interval'
METHOD_OPTIONS = 'methodSpecificOptions'
TIME_KEYS = [
 UPDATE_RATE, LOOKBACK_RANGE, FORECAST_RANGE, FORECAST_INTERVAL]

class Job(threading.Thread):

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self._Job__stop_event = threading.Event()
        self._Job__host = config[0]
        self._Job__service = config[1]
        self._Job__command = config[2]['command']
        self._Job__config = config[2]
        self._Job__update_rates = []
        for p in self._Job__config['perf_labels']:
            for c in self._Job__config['config']:
                if p == c[LABEL]:
                    if self.get_method(c) in MethodCollector.classes.keys():
                        self._Job__update_rates.append((string_to_ms(c[UPDATE_RATE]), c))
                    else:
                        logging.warning('for ' + c[METHOD] + ' does no class exist')

        for u in self._Job__update_rates:
            for k, v in u[1].items():
                if k in TIME_KEYS:
                    u[1][k] = string_to_ms(v)

        self._Job__update_rates = sorted(self._Job__update_rates, key=lambda x: x[0])

    def stop(self):
        self._Job__stop_event.set()

    def run(self):
        if len(self._Job__update_rates) == 0:
            return
        self._Job__stop_event.wait(randint(0, 120))
        while not self._Job__stop_event.is_set():
            start = time.time()
            for update in self._Job__update_rates:
                rate = update[0]
                now = time.time()
                time_to_wait = round(start - now + rate / 1000, 0)
                interrupt = self._Job__stop_event.wait(time_to_wait)
                if interrupt:
                    return
                    try:
                        self.start_calculation(update[1])
                    except URLError as e:
                        logging.getLogger(__name__).error('Could not connect to InfluxDB: ' + str(e))
                    except:
                        logging.getLogger(__name__).error('Job execution failed', exc_info=True)

    def start_calculation(self, conf):
        start = time.time()
        lookback_data = InfluxDBReader.request_past(host=self._Job__host, service=self._Job__service, performance_label=conf[LABEL], lookback=conf[LOOKBACK_RANGE])
        if not lookback_data:
            return
        if log_peformance():
            logging.getLogger(__name__).debug('Fetching data of %s %s %s: %s took %dms' % (
             self._Job__host, self._Job__service, conf[LABEL], self.get_method(conf), delta_ms(start)))
        start = time.time()
        my_class = MethodCollector.classes[self.get_method(conf)]
        if 'calc_forecast' in dir(my_class):
            forecast_data = my_class.calc_forecast(options=conf[METHOD_OPTIONS], forecast_start=self.calc_start_date(lookback_data[(len(lookback_data) - 1)][0], conf[FORECAST_INTERVAL]), forecast_range=conf[FORECAST_RANGE], forecast_interval=conf[FORECAST_INTERVAL], lookback_range=conf[LOOKBACK_RANGE], lookback_data=lookback_data)
            if log_peformance():
                logging.getLogger(__name__).debug('Calculation data of %s %s %s: %s took %dms' % (
                 self._Job__host, self._Job__service, conf[LABEL], self.get_method(conf), delta_ms(start)))
            start = time.time()
            if forecast_data:
                InfluxDBWriter.write_forecast(data=forecast_data, host=self._Job__host, service=self._Job__service, performance_label=conf[LABEL])
                if log_peformance():
                    logging.getLogger(__name__).debug('Writing data of %s %s %s: %s took %dms' % (
                     self._Job__host, self._Job__service, conf[LABEL], self.get_method(conf), delta_ms(start)))
            else:
                logging.getLogger(__name__).debug('Calculation did not return any data: %s %s %s: %s' % (
                 self._Job__host, self._Job__service, conf[LABEL], self.get_method(conf)))
        else:
            if 'search_anomaly' in dir(my_class):
                anomaly_data = my_class.search_anomaly(options=conf[METHOD_OPTIONS], lookback_range=conf[LOOKBACK_RANGE], lookback_data=lookback_data)
                if log_peformance():
                    logging.getLogger(__name__).debug('Calculation data of %s %s %s: %s took %dms' % (
                     self._Job__host, self._Job__service, conf[LABEL], self.get_method(conf), delta_ms(start)))
                if anomaly_data:
                    pass
                InfluxDBWriter.write_anomaly(data=anomaly_data, host=self._Job__host, service=self._Job__service, performance_label=conf[LABEL])
                if log_peformance():
                    logging.getLogger(__name__).debug('Writing data of %s %s %s: %s took %dms' % (
                     self._Job__host, self._Job__service, conf[LABEL], self.get_method(conf), delta_ms(start)))
            else:
                logging.getLogger(__name__).debug('Calculation did not return any data: %s %s %s: %s' % (
                 self._Job__host, self._Job__service, conf[LABEL], self.get_method(conf)))

    @staticmethod
    def get_method(c):
        if python_3():
            method_name = c[METHOD]
        else:
            method_name = c[METHOD].encode('utf8')
        return str.lower(method_name)

    @staticmethod
    def calc_start_date(last_data_point, interval):
        return math.ceil(float(last_data_point) / interval) * interval