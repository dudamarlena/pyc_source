# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyinstruments\datalogger\admin.py
# Compiled at: 2013-08-28 12:58:30
from django.contrib import admin
from pyinstruments.datalogger.models import MeasurementPoint, Sensor
admin.site.register(MeasurementPoint)
admin.site.register(Sensor)