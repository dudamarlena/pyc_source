# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyinstruments\datalogger\admin.py
# Compiled at: 2013-08-28 12:58:30
from django.contrib import admin
from pyinstruments.datalogger.models import MeasurementPoint, Sensor
admin.site.register(MeasurementPoint)
admin.site.register(Sensor)