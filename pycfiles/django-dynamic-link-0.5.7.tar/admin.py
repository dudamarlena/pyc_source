# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/django-dynamic-link/dynamicLink/admin.py
# Compiled at: 2013-04-23 04:13:01
__author__ = 'Andreas Fritz - sources.e-blue.eu'
__copyright__ = 'Copyright (c) ' + '28.08.2010' + ' Andreas Fritz'
__licence__ = 'New BSD Licence'
from django.contrib import admin
from models import Download
from django.utils.translation import ugettext_lazy as _
import api, presettings

class DownLinkAdmin(admin.ModelAdmin):

    def queryset(self, request):
        """catch the request object for list pages"""
        self.request = request
        return super(DownLinkAdmin, self).queryset(request)

    list_display = ('slug', 'active', 'file', 'valid', 'clicks', 'timestamp_creation',
                    'link')
    actions = ['make_link']
    search_fields = ['slug', 'file_path', 'timestamp_creation', 'link_key']
    list_per_page = 50
    fieldsets = (
     (
      _('Link'),
      {'fields': ('slug', 'file_path')}),
     (
      _('Additional values'),
      {'classes': ('collapse', ), 
         'fields': ('active', 'current_clicks', 'timeout_hours', 'max_clicks')}))

    def valid(self, obj):
        """Shows time stamp expired or active time"""
        diff = unicode(obj.get_timout_time()).split('.')[0]
        if obj.timeout_time():
            if obj.active:
                obj.active = False
                obj.save()
            return '<span style="color: #FF7F00; ">%s</span>:<br/> ' % unicode(_('timeout')) + diff
        else:
            return diff

    valid.allow_tags = True
    valid.short_description = _('valid')

    def file(self, obj):
        """Shows truncated filename on platform independent length."""
        return unicode(obj.file_path).split(presettings.DYNAMIC_LINK_MEDIA)[(-1)]

    file.allow_tags = True
    file.short_description = _('file')

    def clicks(self, obj):
        """Shows current and max allowed clicks in the list display"""
        txt = '%s %s %s' % (obj.current_clicks, unicode(_('from')),
         obj.max_clicks)
        if obj.timeout_clicks():
            if obj.active == True:
                obj.active = False
                obj.save()
            return '<span style="color: #FF7F00; ">%s</span><br/>%s' % (
             unicode(_('max clicks reached')), txt)
        else:
            if obj.max_clicks == 0:
                return '%s %s <span style="color: #FF7F00; ">%s</span>' % (
                 obj.current_clicks, unicode(_('from')),
                 unicode(_('unlimited')))
            return txt

    clicks.allow_tags = True
    clicks.short_description = _('clicks')

    def link(self, obj):
        """Generate site and download url from link object"""
        siteurl = api.DownloadSiteUrl([obj.link_key])
        sitelink = siteurl.get_site_url(self.request)
        sitelink = '<span style="color: #FF7F00; ">%s:</span>         <a target="new" href="%s/">%s/</a><br/>' % (
         unicode(_('Site')), sitelink, sitelink)
        filelink = api.file_link_url(self.request, obj)
        filelink = '<span style="color: #FF7F00; ">%s:</span> %s' % (
         unicode(_('File')), filelink)
        return sitelink + filelink

    link.allow_tags = True
    link.short_description = _('link')

    def make_link(modeladmin, request, queryset):
        """Action method. Make site url from many singles objects."""
        li = []
        for obj in queryset:
            li.append(obj.link_key)

        siteurl = api.DownloadSiteUrl(li)
        sitelink = siteurl.get_site_url(request)
        from django.http import HttpResponse
        return HttpResponse('<a target="new" href="%s/">%s/</a><br/>' % (
         sitelink, sitelink))

    make_link.short_description = _('Make from selected a download site link')


admin.site.register(Download, DownLinkAdmin)