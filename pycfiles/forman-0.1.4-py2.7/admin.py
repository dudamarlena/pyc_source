# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/forman/admin.py
# Compiled at: 2017-05-08 12:16:33
from django.contrib import admin
from models import *

class InputInline(admin.StackedInline):
    model = Input


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('header_message', 'download_submission', 'submissions_count')
    inlines = [InputInline]
    model = Survey


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Input)