# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddmonitoring/utils/monitoring_bot.py
# Compiled at: 2019-11-29 13:59:39
# Size of source mod 2**32: 3888 bytes
import requests, numpy as np
from datetime import datetime

class MonitoringBot:

    def __init__(self, url, check_intervals, logger):
        self.logger = logger
        self.check_intervals = []
        self.url = url
        self.metrics = {}
        self.res_data = np.array([])
        self.MAX_SECONDS = 3600
        self.ALERT_INTERVAL = 60
        self.alerts = []

    def get_call(self):
        url = self.url
        req_time = datetime.now()
        if not url.startswith('https://'):
            if not url.startswith('http://'):
                url = 'http://' + url
        self.logger.debug('requesting ' + url)
        res = requests.get(url)
        resp_time = res.elapsed.total_seconds()
        return (res, req_time)

    def update_res_data(self):
        res, call_time = self.get_call()
        MAX_SECONDS = self.MAX_SECONDS
        self.res_data = np.append(self.res_data, [
         {'call_time':call_time, 
          'resp_time':round(res.elapsed.total_seconds() * 1000, 2), 
          'status':res.status_code}])
        now = datetime.now()
        call_time = self.res_data[0]['call_time']
        if (now - call_time).total_seconds() // MAX_SECONDS >= 1:
            self.res_data = self.res_data[1:]

    def make_metrics(self, interval_s):
        now = datetime.now()
        self._init_metric_interval(interval_s)
        data_considered = [data for data in self.res_data if (now - data['call_time']).total_seconds() <= interval_s]
        metrics = self.metrics[interval_s]
        n_calls = len(data_considered)
        max_time = metrics['max_resp_time']
        min_time = metrics['min_resp_time']
        total_res_time = 0
        metrics['200_count'] = 0
        for data in data_considered:
            resp_time = data['resp_time']
            total_res_time += resp_time
            code_count_string = '{}_count'.format(data['status'])
            if code_count_string in metrics:
                metrics[code_count_string] += 1
            else:
                metrics[code_count_string] = 1
            max_time = max(max_time, resp_time)
            min_time = min(min_time, resp_time)

        metrics['avg_resp_time'] = round(total_res_time / n_calls, 2) if n_calls > 0 else 'unknown'
        metrics['max_resp_time'] = max_time
        metrics['min_resp_time'] = min_time
        metrics['total_requests'] = n_calls
        if interval_s == self.ALERT_INTERVAL:
            self.handle_alerts()
        metrics['availability'] = round(metrics['200_count'] / n_calls * 100, 2) if n_calls > 0 else 'unknown'

    def handle_alerts(self):
        metrics = self.metrics[self.ALERT_INTERVAL]
        if metrics['prev_availability'] == -1:
            if metrics['availability'] == -1:
                return
        if metrics['prev_availability'] == -1:
            metrics['prev_availability'] = metrics['availability']
            return
        if metrics['prev_availability'] > 80:
            if metrics['availability'] < 80:
                self.alerts.append(self.make_alert('DOWN'))
        if metrics['prev_availability'] < 80:
            if metrics['availability'] > 80:
                self.alerts.append(self.make_alert('UP'))

    def make_alert(self, status):
        return '{} is {} @ {}'.format(self.url, status, datetime.now().isoformat())

    def _init_metric_interval(self, interval_s):
        self.metrics[interval_s] = {'avg_resp_time':0, 
         'max_resp_time':0, 
         'min_resp_time':float('inf'), 
         'availability':-1, 
         '200_count':0, 
         'total_requests':0}
        if interval_s == self.ALERT_INTERVAL:
            self.metrics[interval_s]['prev_availability'] = -1