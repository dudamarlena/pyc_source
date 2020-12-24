# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jmbo_facebook/admin.py
# Compiled at: 2013-05-14 09:27:46
from django.contrib import admin
from jmbo.admin import ModelBaseAdmin
from jmbo_facebook import models

class PageAdmin(ModelBaseAdmin):
    list_display = ModelBaseAdmin.list_display + ('facebook_id', 'access_token')


admin.site.register(models.Page, PageAdmin)