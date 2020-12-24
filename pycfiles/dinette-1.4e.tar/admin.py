# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/javed/Work/Dinette/dinette/admin.py
# Compiled at: 2013-07-02 04:51:32
from django.contrib import admin
from dinette import models
admin.site.register(models.SuperCategory)
admin.site.register(models.Category)
admin.site.register(models.Ftopics)
admin.site.register(models.Reply)
admin.site.register(models.DinetteUserProfile)
admin.site.register(models.SiteConfig)
admin.site.register(models.NavLink)