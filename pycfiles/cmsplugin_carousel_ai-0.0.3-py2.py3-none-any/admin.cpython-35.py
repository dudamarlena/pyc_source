# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/admin.py
# Compiled at: 2017-08-31 05:41:42
# Size of source mod 2**32: 1374 bytes
from django.contrib import admin
from publisher.admin import PublisherAdmin, PublisherPublishedFilter
from .models import Article, Category, ArticleAttachment, Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}


class ArticleAttachmentInline(admin.StackedInline):
    model = ArticleAttachment
    extra = 1
    fields = ['name', 'attachment_file']


class ArticleAdmin(PublisherAdmin):
    list_display = ('title', 'slug', 'language', 'author', 'published_from', 'published_until',
                    'publisher_publish', 'publisher_status')
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = [
     'tags']
    list_filter = ['language', 'category', 'tags', PublisherPublishedFilter]
    inlines = [ArticleAttachmentInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        return form


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)