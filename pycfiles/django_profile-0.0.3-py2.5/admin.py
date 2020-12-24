# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/profile/admin.py
# Compiled at: 2010-08-04 04:05:50
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from profile import utils
profile_model = utils.get_profile_model()
if profile_model:

    class ProfileInline(admin.StackedInline):
        model = profile_model


    class UserAdmin(UserAdmin):
        inlines = [
         ProfileInline]


    admin.site.unregister(User)
    admin.site.register(User, UserAdmin)