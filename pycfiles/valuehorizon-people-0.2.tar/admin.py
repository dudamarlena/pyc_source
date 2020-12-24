# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/quincy/Code/valuehorizon-people/people/admin.py
# Compiled at: 2015-01-16 14:30:02
from django.contrib import admin
from people.models import Person
from countries.models import Country

class PersonAdmin(admin.ModelAdmin):
    search_fields = [
     'first_name', 'last_name']
    filter_horizontal = ['nationality']


admin.site.register(Person, PersonAdmin)