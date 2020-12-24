# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/miscprom/exporters/wanikani.py
# Compiled at: 2018-11-08 07:12:47
# Size of source mod 2**32: 1111 bytes
import requests
from miscprom.core.util import Collector
from prometheus_client.core import GaugeMetricFamily

class VersionOne(Collector):

    def get(self, url):
        response = requests.get(url.format(self.view.apikey))
        response.raise_for_status()
        return response.json()

    def collect(self):
        data = self.get('https://www.wanikani.com/api/user/{}/study-queue')
        yield GaugeMetricFamily('wanikani_level', 'Level', value=(data['user_information']['level']))
        yield GaugeMetricFamily('wanikani_lessons', 'Level', value=(data['requested_information']['lessons_available']))
        yield GaugeMetricFamily('wanikani_reviews', 'Level', value=(data['requested_information']['reviews_available']))
        data = self.get('https://www.wanikani.com/api/user/{}/srs-distribution')
        levels = GaugeMetricFamily('wanikani_items', 'Levels of current items', labels=['level', 'item'])
        for level, items in data['requested_information'].items():
            for item, count in items.items():
                levels.add_metric([item, level], count)

        yield levels