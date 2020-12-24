# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/skylar/pinax/projects/testoster/apps/listings/admin.py
# Compiled at: 2009-08-16 07:20:42
from django.contrib import admin
from listings.models import Listing

class ListingAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'description', 'want', 'state')
    list_filter = ('owner', 'state')
    search_fields = ('title', 'description', 'want')


admin.site.register(Listing, ListingAdmin)