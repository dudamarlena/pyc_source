# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nijel/weblate/weblate/weblate/fonts/admin.py
# Compiled at: 2020-03-12 04:44:13
# Size of source mod 2**32: 1486 bytes
from django.contrib import admin
from weblate.fonts.models import FontOverride
from weblate.wladmin.models import WeblateModelAdmin

class FontAdmin(WeblateModelAdmin):
    list_display = [
     'family', 'style', 'project', 'user']
    search_fields = ['family', 'style']
    list_filter = [('project', admin.RelatedOnlyFieldListFilter)]
    ordering = ['family', 'style']


class InlineFontOverrideAdmin(admin.TabularInline):
    model = FontOverride
    extra = 0


class FontGroupAdmin(WeblateModelAdmin):
    list_display = [
     'name', 'font', 'project']
    search_fields = ['name', 'font__family']
    list_filter = [('project', admin.RelatedOnlyFieldListFilter)]
    ordering = ['name']
    inlines = [InlineFontOverrideAdmin]