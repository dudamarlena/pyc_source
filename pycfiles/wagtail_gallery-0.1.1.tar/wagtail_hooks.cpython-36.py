# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/gallery/base/wagtail_gallery/wagtail_gallery/wagtail_hooks.py
# Compiled at: 2018-10-05 03:06:05
# Size of source mod 2**32: 1214 bytes
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from .models import GalleryPage, Category

class GalleryPageModelAdmin(ModelAdmin):
    __doc__ = 'Makes the adding of gallery pages easy by providing a hook to the menu system thus not needing to use the page hierarchy'
    model = GalleryPage
    menu_label = _('Gallery')
    menu_icon = 'picture'
    list_display = ('first_published_at', 'title', 'description', 'categories')
    list_filter = ('first_published_at', 'categories')
    search_fields = ('title', 'description', 'first_published_at')


class GalleryCategoryAdmin(ModelAdmin):
    __doc__ = 'Makes the adding of categories simply by giving own menu entry'
    model = Category
    menu_label = _('Categories')
    menu_icon = 'group'
    list_display = ('name', )
    search_fields = ('name', )


class GalleryModelAdminGroup(ModelAdminGroup):
    __doc__ = 'Creates the side menu entry with the two other ModelAdmins inside of it'
    menu_label = _('Gallery')
    menu_icon = 'picture'
    menu_order = 300
    items = (GalleryPageModelAdmin, GalleryCategoryAdmin)


modeladmin_register(GalleryModelAdminGroup)