# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ooyala/admin.py
# Compiled at: 2011-01-27 11:10:56
from django.contrib import admin
from ooyala.models import OoyalaItem, UrlVideoLink, VideoPage, OoyalaChannelList
from ooyala.library import OoyalaQuery

class OoyalaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'content_type', 'nice_length', 'tags')
    list_filter = ('content_type', 'status')
    search_fields = ('title', 'description')


class LinkAdmin(admin.ModelAdmin):
    search_fields = ('item__title', 'url')
    list_display = ('url', 'item')


class PageAdmin(admin.ModelAdmin):
    search_fields = ('url', )
    list_display = ('url', )
    filter_horizontal = ('items', )


class ChannelAdmin(admin.ModelAdmin):
    search_fields = ('channel__title', )
    list_display = ('channel', 'total_items')
    filter_horizontal = ('videos', )


admin.site.register(OoyalaChannelList, ChannelAdmin)
admin.site.register(OoyalaItem, OoyalaItemAdmin)
admin.site.register(UrlVideoLink, LinkAdmin)
admin.site.register(VideoPage, PageAdmin)