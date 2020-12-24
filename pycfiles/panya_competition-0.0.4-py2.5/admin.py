# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/competition/admin.py
# Compiled at: 2010-08-04 03:48:25
from django.contrib import admin
from panya.admin import ModelBaseAdmin
from competition.models import Competition, CompetitionEntry, CompetitionPreferences
admin.site.register(Competition, ModelBaseAdmin)
admin.site.register(CompetitionEntry)
admin.site.register(CompetitionPreferences)