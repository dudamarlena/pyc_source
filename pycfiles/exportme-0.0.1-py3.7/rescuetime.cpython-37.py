# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/miscprom/exporters/rescuetime.py
# Compiled at: 2018-11-08 07:12:47
# Size of source mod 2**32: 618 bytes
import requests
from miscprom.core.util import Collector
from prometheus_client.core import GaugeMetricFamily

class RescueTime(Collector):

    def collect(self):
        response = requests.get('https://www.rescuetime.com/anapi/daily_summary_feed', params={'key': self.view.apikey})
        response.raise_for_status()
        data = response.json()[0]
        print(data)
        yield GaugeMetricFamily('rescutime_pulse', 'Productivity Pulse', value=(data['productivity_pulse']))
        yield GaugeMetricFamily('rescuetime_uncatagorized', 'Unknown', value=(data['uncategorized_hours'] * 60))