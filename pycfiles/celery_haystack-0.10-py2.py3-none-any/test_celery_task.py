# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/brent/anaconda/envs/fba/lib/python2.7/site-packages/examples/strait_celery/test_celery_task.py
# Compiled at: 2014-08-11 23:58:05
import sys
from celery import Celery
from celery_geolocator.tasks import geocode
__author__ = 'brent'
app = Celery()
app.config_from_object('examples.strait_celery.celeryconfig')
for arg in sys.argv[1:]:
    print 'geocoding', arg
    v = geocode.delay(arg)
    print v.get()