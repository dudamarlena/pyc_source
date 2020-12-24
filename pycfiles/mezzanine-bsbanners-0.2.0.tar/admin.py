# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/alan/projects/mldemo-po/mezzanine_bsbanners/admin.py
# Compiled at: 2018-11-16 08:16:10
"""
Mezzanine BS Banners
Making it easier to manage attention grabbing and compelling banners
"""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from mezzanine_bsbanners.models import Banners, Slides

class SlidesInline(admin.StackedInline):
    """
    Inline Slides Admin class
    """
    model = Slides
    extra = 1
    fieldsets = (
     (
      None,
      {b'fields': [
                   b'title', b'show_title',
                   b'content',
                   b'cta', b'buttontype',
                   b'image', b'link_url',
                   b'status']}),)


class BannersAdmin(admin.ModelAdmin):
    """
    Admin class for Banners
    """
    list_display = ('title', 'slug', 'status')
    list_editable = ('status', )
    fieldsets = (
     (
      None,
      {b'fields': [
                   b'title', b'bannertype']}),
     (
      _(b'Advanced data'),
      {b'fields': [
                   b'slug',
                   b'buttonsize', b'ctachevron',
                   b'interval', b'wrap', b'pause',
                   b'showindicators', b'animate',
                   b'status'], 
         b'classes': ('collapse-closed', )}))
    inlines = [
     SlidesInline]


admin.site.register(Banners, BannersAdmin)