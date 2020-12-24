# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/alan/projects/mldemo-po/mezzanine_bsbanners/admin.py
# Compiled at: 2019-02-28 08:09:26
# Size of source mod 2**32: 1639 bytes
"""
Mezzanine BS Banners
Making it easier to manage attention grabbing and compelling banners
"""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from mezzanine_bsbanners.models import Banners, Slides

class SlidesInline(admin.StackedInline):
    __doc__ = '\n    Inline Slides Admin class\n    '
    model = Slides
    extra = 1
    fieldsets = (
     (
      None,
      {'fields': [
                  'title', 'show_title',
                  'content',
                  'cta', 'buttontype',
                  'image', 'link_url',
                  'status']}),)


class BannersAdmin(admin.ModelAdmin):
    __doc__ = '\n    Admin class for Banners\n    '
    list_display = ('title', 'slug', 'status')
    list_editable = ('status', )
    fieldsets = (
     (
      None,
      {'fields': ['title', 'bannertype']}),
     (
      _('Advanced data'),
      {'fields':[
        'slug',
        'buttonsize', 'ctachevron',
        'interval', 'wrap', 'pause',
        'showindicators', 'animate',
        'carouseltransition',
        'status'], 
       'classes':('collapse-closed', )}))
    inlines = [
     SlidesInline]


admin.site.register(Banners, BannersAdmin)