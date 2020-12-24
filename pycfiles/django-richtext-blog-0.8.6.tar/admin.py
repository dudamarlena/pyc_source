# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/projects/wholebaked-site/venv/lib/python2.7/site-packages/richtext_blog/admin.py
# Compiled at: 2012-04-15 01:39:30
from django.contrib import admin
from models import Post, Comment, Tag
from forms import PostFormAdmin

class CommentInline(admin.TabularInline):
    """
    Inline definition for comments
    """
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    form = PostFormAdmin
    fields = ('title', 'slug', 'tags', 'content', 'comments_closed')
    search_fields = ('title', )
    list_display = ('title', 'author', 'created', 'modified', 'number_of_comments',
                    'comments_closed', 'tag_list_str')
    list_editable = ('comments_closed', )
    list_filter = ('author__username', 'tags')
    inlines = (CommentInline,)

    def save_model(self, request, obj, form, change):
        """
        Override save_model method to allow automatic population of the author
        field with the current user
        """
        obj.author = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        """
        Save changed inline objects (ie Comments)
        This is so if the logged in user saves a comment in the admin interface
        the user can be logged against the Comment object.
        """
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Comment):
                instance.auth_user = request.user
            instance.save()


admin.site.register(Post, PostAdmin)

class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)