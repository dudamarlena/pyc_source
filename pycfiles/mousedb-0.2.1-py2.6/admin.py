# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/timed_mating/admin.py
# Compiled at: 2010-06-14 19:51:43
"""Settings to control the admin interface for the timed_mating app.

This file defines a PlugEventsAdmin object to enter parameters about individual plug events/"""
from django.contrib import admin
from mousedb.timed_mating.models import PlugEvents

class PlugEventsAdmin(admin.ModelAdmin):
    """This class defines the admin interface for the PlugEvents model."""
    list_display = ('PlugDate', 'PlugFemale', 'PlugMale', 'SacrificeDate', 'Researcher',
                    'Active')


admin.site.register(PlugEvents, PlugEventsAdmin)