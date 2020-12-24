# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django-flatpages-extension/django-flatpages-extension/admin.py
# Compiled at: 2018-07-10 12:52:03
# Size of source mod 2**32: 420 bytes
from django.contrib import admin
from .forms import FlatpageExtendedForm
from .models import FlatPageExtended
from django.contrib.flatpages.admin import FlatPageAdmin
FlatPageAdmin.fieldsets[0][1]['fields'] = ('url', 'meta_title', 'meta_keywords', 'meta_description',
                                           'title', 'content', 'sites')

@admin.register(FlatPageExtended)
class FlatPageAdminExtended(FlatPageAdmin):
    form = FlatpageExtendedForm