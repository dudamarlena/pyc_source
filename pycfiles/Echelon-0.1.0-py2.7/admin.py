# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/echelon/admin.py
# Compiled at: 2011-09-24 06:25:11
from django import forms
from django.contrib import admin
from django.conf.urls.defaults import patterns
from django.views.generic.list_detail import object_detail
from echelon.models import Category, Page, SiteSettings, SiteVariable

class MDPreview(admin.ModelAdmin):

    def md_preview(self, obj):
        return '<div class="livepreview" id="#id_content">Preview</div>'

    md_preview.allow_tags = True
    md_preview.short_description = 'Preview'

    class Media:
        js = ('/media/javascripts/jquery.js', '/media/javascripts/showdown.js', '/media/javascripts/jquery.mdpreview.js')


class CategoryAdmin(MDPreview, admin.ModelAdmin):
    list_display = ('title', 'desc', 'content')
    readonly_fields = ('md_preview', )


class PageAdmin(MDPreview, admin.ModelAdmin):
    list_display = ('title', 'content', 'script')
    readonly_fields = ('md_preview', )


class SiteSettingsAdmin(admin.ModelAdmin):
    filter_list = ('global_javascript', )


class SiteVariableAdmin(admin.ModelAdmin):
    fields = ('name', 'value')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(SiteVariable, SiteVariableAdmin)