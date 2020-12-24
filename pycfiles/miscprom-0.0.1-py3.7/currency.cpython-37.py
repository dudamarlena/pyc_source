# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/miscprom/exporters/currency.py
# Compiled at: 2018-11-08 07:24:09
# Size of source mod 2**32: 635 bytes
import requests
from prometheus_client.core import GaugeMetricFamily
from miscprom.core.util import Collector

class Currency(Collector):

    def collect(self):
        url = 'https://openexchangerates.org/api/latest.json'
        result = requests.get(url, params={'app_id': self.view.apikey})
        result.raise_for_status()
        json = result.json()
        metric = GaugeMetricFamily('currency_rate',
          'Currency Rate', labels=['source', 'destination'])
        metric.add_metric(['usd', 'jpy'], json['rates']['JPY'])
        metric.add_metric(['usd', 'eur'], json['rates']['EUR'])
        yield metric