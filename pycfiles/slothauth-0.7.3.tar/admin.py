# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/slothauth/admin.py
# Compiled at: 2016-02-01 18:16:07
from django.contrib import admin
from django.contrib.auth import get_user_model
Account = get_user_model()

class SlothAuthBaseUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = [
     'id', 'email']

    class Meta:
        model = Account