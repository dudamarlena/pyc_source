# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/leocornus/django/ploneproxy/admin.py
# Compiled at: 2010-06-01 17:20:12
"""
registering models to Django default admin interface.
"""
from django.contrib import admin
from django.contrib.sessions.models import Session
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

class SessionAdmin(admin.ModelAdmin):
    """
    admin class for Session model
    """
    __module__ = __name__
    list_display = ('expire_date', 'session_key')
    list_filter = ('expire_date', )
    ordering = ('expire_date', )


admin.site.register(Session, SessionAdmin)