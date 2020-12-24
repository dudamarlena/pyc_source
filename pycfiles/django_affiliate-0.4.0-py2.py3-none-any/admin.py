# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stalk/develop/django_affiliate/django-affiliate/affiliate/admin.py
# Compiled at: 2015-11-02 07:10:37
from django.contrib import admin
from .utils import get_model
from . import app_settings
Affiliate = get_model(app_settings.AFFILIATE_MODEL)

class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'is_active', 'reward_amount', 'reward_percentage',
                    'created_at')
    raw_id_fields = ('user', )


admin.site.register(Affiliate, AffiliateAdmin)