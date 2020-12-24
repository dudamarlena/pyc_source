# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/ease_restapi/demo/admin.py
# Compiled at: 2015-01-25 06:15:54
__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'
from django.contrib import admin
from .models import RingInfo

class RingInfoAdmin(admin.ModelAdmin):
    """自定义ModelAdmin.
    """
    list_display = ('id', 'user', 'username', 'password', 'status', 'add_date')
    ordering = ('-id', )
    list_filter = ('status', 'add_date')
    search_fields = ('user__username', 'username')


admin.site.register(RingInfo)