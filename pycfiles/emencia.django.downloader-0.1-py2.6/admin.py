# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia/django/downloader/admin.py
# Compiled at: 2010-04-27 13:28:02
"""Admin for emencia.django.downloader"""
from django.contrib import admin
from django.utils.translation import ugettext as _
from emencia.django.downloader.models import Download

class DownloadAdmin(admin.ModelAdmin):
    list_display = ('filename', 'slug', 'creation')


admin.site.register(Download, DownloadAdmin)