# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/peter/projects/thalesians/menuplaceholder/menuplaceholder/admin.py
# Compiled at: 2018-04-01 02:13:50
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from .models import MenuPlaceholder
admin.site.register(MenuPlaceholder, PageAdmin)