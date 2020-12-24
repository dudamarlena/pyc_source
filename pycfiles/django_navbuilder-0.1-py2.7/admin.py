# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/navbuilder/admin.py
# Compiled at: 2017-07-06 08:35:55
from django.contrib import admin
from navbuilder.forms import MenuAdminForm, MenuItemAdminForm
from navbuilder.models import Menu, MenuItem

class MenuItemInline(admin.StackedInline):
    form = MenuItemAdminForm
    model = MenuItem
    fk_name = 'menu'
    prepopulated_fields = {'slug': ['title']}


class MenuAdmin(admin.ModelAdmin):
    form = MenuAdminForm
    list_display = ['title']
    inlines = [MenuItemInline]
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title', 'slug']


class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemAdminForm
    list_display = ['title', 'slug', 'parent', '_get_absolute_url']
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title', 'slug']
    list_filter = ['menu']
    raw_id_fields = ('parent', )

    def _get_absolute_url(self, obj):
        try:
            url = obj.link.get_absolute_url()
        except AttributeError:
            url = None

        if url:
            return '<a href="%s" target="public">%s</a>' % (url, url)
        else:
            return '<p class="errornote">Inactive or broken link</p>'

    _get_absolute_url.short_description = 'Permalink'
    _get_absolute_url.allow_tags = True


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)