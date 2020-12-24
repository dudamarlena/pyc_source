# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialauth/admin.py
# Compiled at: 2010-06-28 10:33:16
from socialauth.models import AuthMeta, OpenidProfile, TwitterUserProfile, FacebookUserProfile, LinkedInUserProfile
from django.contrib import admin
admin.site.register(AuthMeta)
admin.site.register(OpenidProfile)
admin.site.register(TwitterUserProfile)
admin.site.register(FacebookUserProfile)
admin.site.register(LinkedInUserProfile)