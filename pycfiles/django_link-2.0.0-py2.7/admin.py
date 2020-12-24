# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-link/link/admin.py
# Compiled at: 2017-07-06 07:47:29
from django.contrib import admin
from link.forms import LinkAdminForm
from link.models import Link, ViewParam

class LinkAdmin(admin.ModelAdmin):
    form = LinkAdminForm
    list_display = ('title', '_get_absolute_url')
    prepopulated_fields = {'slug': ['title']}
    filter_horizontal = ['view_params']
    search_fields = [
     'title', 'slug', 'url']

    def _get_absolute_url(self, obj):
        url = obj.get_absolute_url()
        if url:
            return '<a href="%s" target="public">%s</a>' % (url, url)
        return '<p class="errornote">Inactive or broken link</p>'

    _get_absolute_url.short_description = 'Permalink'
    _get_absolute_url.allow_tags = True


admin.site.register(Link, LinkAdmin)
admin.site.register(ViewParam)