# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/miscprom/wanikani/views.py
# Compiled at: 2018-11-08 07:04:52
# Size of source mod 2**32: 1470 bytes
from django.http import HttpResponse
from django.views import View
import requests
from prometheus_client import CollectorRegistry, generate_latest
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from . import models

class Metrics(View):

    def collect(self):
        apikey = models.APIKey.objects.first()
        headers = {'Authorization': 'Bearer %s' % apikey.key}
        response = requests.get('https://api.wanikani.com/v2/user', headers=headers)
        response.raise_for_status()
        data = response.json()
        yield GaugeMetricFamily('wanikani_level', 'Level', value=(data['data']['level']))
        response = requests.get('https://api.wanikani.com/v2/summary', headers=headers)
        response.raise_for_status()
        data = response.json()
        lessons = 0
        for entry in data['data']['lessons']:
            lessons += len(entry['subject_ids'])

        yield GaugeMetricFamily('wanikani_lessons', 'Lessons', value=lessons)
        reviews = 0
        for entry in data['data']['reviews']:
            reviews += len(entry['subject_ids'])

        yield GaugeMetricFamily('wanikani_reviews', 'reviews', value=reviews)

    def get(self, request):
        registry = CollectorRegistry()
        registry.register(self)
        return HttpResponse((generate_latest(registry)), content_type='text/plain')