# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tagbase\gutentag\admin.py
# Compiled at: 2009-07-13 23:06:10
from tagbase.gutentag.models import Gene, Tags, Genetag, Seq
from django.contrib import admin

class GenetagInline(admin.TabularInline):
    model = Genetag
    extra = 1


class SeqInline(admin.TabularInline):
    model = Seq
    max_num = 2


class GeneAdmin(admin.ModelAdmin):
    inlines = [
     SeqInline]
    list_display = [
     'descript', 'orgn']
    search_fields = ['descript']


admin.site.register(Gene, GeneAdmin)

class TagsAdmin(admin.ModelAdmin):
    inlines = [
     GenetagInline]
    list_display = ('tag_type', 'tag_acc', 'tag_name', 'tag_details')
    search_fields = ['tag_name', 'tag_acc', 'tag_details', 'tag_type']


admin.site.register(Tags, TagsAdmin)