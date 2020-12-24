# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/christianschuermann/Documents/Repositories/django-translator/translator/admin.py
# Compiled at: 2020-01-24 09:57:20
# Size of source mod 2**32: 1301 bytes
from django.conf import settings
from django.contrib import admin
import django.utils.translation as _
from modeltranslation.admin import TranslationAdmin
from translator.models import Translation
CATEGORY_SEPARATOR = getattr(settings, 'DJANGO_TRANSLATOR_CATEGORY_SEPARATOR', '__')

class KeyFilter(admin.SimpleListFilter):
    title = _('Categories')
    parameter_name = 'keys'

    def lookups(self, request, model_admin):
        queryset = model_admin.model.objects.filter(key__contains=CATEGORY_SEPARATOR).values_list('key', flat=True)
        unique_categories = {key.split(CATEGORY_SEPARATOR)[0] for key in queryset}
        categories = sorted([key for key in unique_categories])
        return ((
         category, category) for category in categories)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(key__startswith=(self.value()))
        return queryset


class TranslationAdministration(TranslationAdmin):
    list_filter = (
     KeyFilter, 'tags')
    search_fields = ['key', 'description']
    ordering = ('key', )
    list_display = ('key', 'description')
    list_editable = ('description', )


admin.site.register(Translation, TranslationAdministration)