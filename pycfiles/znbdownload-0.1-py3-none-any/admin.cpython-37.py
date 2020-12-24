# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/project/znbdownload/admin.py
# Compiled at: 2019-07-04 12:33:55
# Size of source mod 2**32: 293 bytes
from django.contrib import admin
from .models import Download, PrivateDownload

class DownloadAdmin(admin.ModelAdmin):
    pass


class PrivateDownloadAdmin(admin.ModelAdmin):
    pass


admin.site.register(Download, DownloadAdmin)
admin.site.register(PrivateDownload, PrivateDownloadAdmin)