# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/dev-p5qc/workspace/python/team_reset/ninecms/admin.py
# Compiled at: 2015-03-24 04:17:47
""" Admin objects declaration for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django.contrib import admin
from ninecms import models
from mptt.admin import MPTTModelAdmin

class PageLayoutElementInline(admin.StackedInline):
    """ Page Layout Element stacked inline to be displayed in Page Types """
    model = models.PageLayoutElement
    extra = 0


class PageTypeAdmin(admin.ModelAdmin):
    """ Get a list of Page Types """
    inlines = [
     PageLayoutElementInline]
    list_display = ('name', 'description')
    search_fields = ['name']


class NodeRevisionInline(admin.StackedInline):
    """ Node Revision stacked inline to be displayed in Nodes (NodeAdmin) """
    model = models.NodeRevision
    extra = 0


class ImageInline(admin.StackedInline):
    """ Images inline to be displayed in Nodes (NodeAdmin) """
    model = models.Image
    extra = 0


class FileInline(admin.StackedInline):
    """ Files inline to be displayed in Nodes (NodeAdmin) """
    model = models.File
    extra = 0


class VideoInline(admin.StackedInline):
    """ Videos inline to be displayed in Nodes (NodeAdmin) """
    model = models.Video
    extra = 0


class NodeAdmin(admin.ModelAdmin):
    """ Get a list of Nodes, also use inlines in Node form """
    inlines = [
     NodeRevisionInline, ImageInline, FileInline, VideoInline]
    list_display = ('title', 'page_type', 'language', 'user', 'status', 'promote',
                    'sticky', 'created', 'changed', 'original_translation')
    list_filter = ['created', 'changed']
    search_fields = ['title', 'summary', 'body', 'highlight']


class NodeRevisionAdmin(admin.ModelAdmin):
    """ Get a list of Node Revisions """
    list_display = ('node', 'user', 'log_entry', 'created', 'title')
    list_filter = ['created']
    search_fields = ['title', 'summary', 'body', 'highlight']


class UrlAliasAdmin(admin.ModelAdmin):
    """ Get a list of Url Aliases """
    list_display = ('language', 'alias', 'node')
    search_fields = ['alias']


class MenuItemAdmin(MPTTModelAdmin):
    """ Get a list of Menu Items """
    list_display = ('title', 'language', 'path', 'parent', 'disabled')
    search_fields = ['path', 'title']


class ContentBlockAdmin(admin.ModelAdmin):
    """ Get a list of blocks """
    list_display = ('type', 'node', 'menu_item', 'signal')


class PageLayoutElementAdmin(admin.ModelAdmin):
    """ Get a list of Page Layout Elements """
    list_display = ('page_type', 'region', 'block', 'weight')
    search_fields = ['region']


class ImageAdmin(admin.ModelAdmin):
    """ Get a list of images """
    list_display = ('node', 'image', 'title', 'group')


class FileAdmin(admin.ModelAdmin):
    """ Get a list of files """
    list_display = ('node', 'file', 'title', 'group')


class VideoAdmin(admin.ModelAdmin):
    """ Get a list of videos """
    list_display = ('node', 'video', 'title', 'group')


class TaxonomyTermAdmin(MPTTModelAdmin):
    """ Get a list of Taxonomy Terms """
    list_display = ('name', 'description_node', 'parent', 'weight')


admin.site.register(models.PageType, PageTypeAdmin)
admin.site.register(models.Node, NodeAdmin)
admin.site.register(models.NodeRevision, NodeRevisionAdmin)
admin.site.register(models.UrlAlias, UrlAliasAdmin)
admin.site.register(models.MenuItem, MenuItemAdmin)
admin.site.register(models.ContentBlock, ContentBlockAdmin)
admin.site.register(models.PageLayoutElement, PageLayoutElementAdmin)
admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.File, FileAdmin)
admin.site.register(models.Video, VideoAdmin)
admin.site.register(models.TaxonomyTerm, TaxonomyTermAdmin)