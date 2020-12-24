# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/event/admin.py
# Compiled at: 2010-08-03 06:21:45
from django.contrib import admin
from panya.admin import ModelBaseAdmin
from event.models import Event, Location, Venue
admin.site.register(Event, ModelBaseAdmin)
admin.site.register(Location)
admin.site.register(Venue)