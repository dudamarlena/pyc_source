# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/djangosampler/test_sampler.py
# Compiled at: 2015-11-17 05:08:04
from time import sleep
from django.conf import settings
from django.test import TestCase
import sampler, models

class TestSampler(TestCase):

    def test_calculate_cost(self):
        settings.DJANGO_SAMPLER_USE_COST = None
        self.assertEquals(0.0, sampler._calculate_cost(1))
        return

    def test_sample(self):
        settings.DJANGO_SAMPLER_USE_COST = True
        sampler.sample('sql', 'SELECT 1', 1, [])
        query = models.Query.objects.get()
        self.assertEquals('sql', query.query_type)
        self.assertEquals('SELECT 1', query.query)


class TestSamplingContextManager(TestCase):

    def test_with(self):
        sampler.FREQ = 1
        with sampler.sampling('bob', 'baz', ('foo', 'foobar')):
            sleep(0.01)
        query = models.Query.objects.get()
        self.assertEquals('bob', query.query_type)
        self.assertEquals('baz', query.query)
        self.assertTrue(query.total_duration >= 0.01)