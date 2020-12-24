# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/repository/admin.py
# Compiled at: 2017-07-10 01:59:22
# Size of source mod 2**32: 482 bytes
from django.contrib import admin
from django.contrib.sites.models import Site
from moneta.repository.models import Element, Repository

class ElementAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Site)
admin.site.register(Element, ElementAdmin)
admin.site.register(Repository)