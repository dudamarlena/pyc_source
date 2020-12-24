# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dynamo\admin.py
# Compiled at: 2011-08-02 15:59:24
from django.contrib import admin
from django import forms
from django.db import models
from dynamo.models import MetaModel, MetaField

class MetaFieldInlineAdmin(admin.StackedInline):
    model = MetaField
    fieldsets = (
     (
      None,
      {'fields': (
                  ('name', 'type', 'related_model'),
                  ('order', 'required', 'default', 'choices'))}),
     (
      'Advanced Options',
      {'fields': (
                  ('verbose_name', 'description'),
                  ('unique', 'unique_together', 'help')), 
         'classes': ('collapse', )}))
    extra = 0


class MetaModelForm(forms.ModelForm):

    class Meta:
        model = MetaModel


class MetaModelAdmin(admin.ModelAdmin):
    model = MetaModel
    form = MetaModelForm
    inlines = [MetaFieldInlineAdmin]
    list_display = ('name', 'description')
    list_display_links = ('name', 'description')
    list_display_editable = ('name', 'description')
    ordering = ('name', )
    fieldsets = (
     (
      None,
      {'fields': (('name', 'description'), )}),
     (
      'Advanced options',
      {'classes': ('collapse', ), 
         'fields': (('app', 'admin'), )}))

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        return super(MetaModelAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)


admin.site.register(MetaModel, MetaModelAdmin)