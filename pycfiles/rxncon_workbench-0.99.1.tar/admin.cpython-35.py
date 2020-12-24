# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mathias/tbp/django_rxncon_site/src/rxncon_system/admin.py
# Compiled at: 2018-06-27 10:02:27
# Size of source mod 2**32: 485 bytes
from django.contrib import admin
try:
    from rxncon_system.models import Rxncon_system
except ImportError:
    from src.rxncon_system.models import Rxncon_system

class RxnconSystemAdmin(admin.ModelAdmin):
    list_display = [
     '__str__', 'project_name', 'project_id']
    list_display_links = ['__str__']
    list_filter = ['updated', 'timestamp']
    search_fields = ['__str__']

    class Meta:
        model = Rxncon_system


admin.site.register(Rxncon_system, RxnconSystemAdmin)