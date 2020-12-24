# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/projects/volunteer-coordination/volunteerhub/apps/volunteers/admin.py
# Compiled at: 2014-06-10 15:49:30
from django.contrib import admin
from .models import Organization, LaborType, Opportunity, Location, Project, VolunteerApplication, Volunteer

class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('address', 'city', 'state')}
    list_display = ('address', 'city', 'state')
    list_filter = ('city', 'state')


admin.site.register(Location, LocationAdmin)
admin.site.register(LaborType)
admin.site.register(Opportunity)
admin.site.register(Organization)
admin.site.register(Project)
admin.site.register(VolunteerApplication)
admin.site.register(Volunteer)