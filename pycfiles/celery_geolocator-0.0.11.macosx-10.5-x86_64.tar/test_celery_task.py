# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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