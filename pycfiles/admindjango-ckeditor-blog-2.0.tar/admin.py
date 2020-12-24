# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/workspace/myproject/dajngoadmin/blog/admin.py
# Compiled at: 2017-06-16 07:05:53
from django.contrib import admin
from blog.models import Blog
import datetime
from django import forms

class BlogForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Blog
        exclude = ('delete', 'soft_delete')


class BlogAdmin(admin.ModelAdmin):
    exclude = ('delete', 'soft_delete')
    search_fields = ('title', )
    fieldsets = (
     (
      'Add Blog',
      {'fields': ('title', 'short_description', 'description', 'upload_image', 'author', 'status')}),
     (
      'Seo Management',
      {'fields': ('meta_title', 'meta_keywords', 'meta_description', 'og_title', 'og_description', 'og_url',
 'meta_robot', 'canonical_url')}))

    def changelist_view(self, request, extra_context=None):
        if request.user.has_perm('blog.can_approve'):
            self.list_display = ('title', 'author', 'status', 'created_date', 'modified_date')
        else:
            self.list_display = ('title', 'author', 'created_date', 'modified_date')
        return super(BlogAdmin, self).changelist_view(request, None)

    def save_model(self, request, obj, form, change):
        date_time = datetime.datetime.now()
        current_year = datetime.datetime.now().year
        if not obj.created_date:
            obj.created_date = date_time
            obj.year = current_year
            obj.modified_date = None
            obj.save()
        if not request.user.has_perm('blog.can_approve'):
            obj.status = False
            obj.year = current_year
            obj.modified_date = None
            obj.save()
        elif obj.status == True:
            obj.year = current_year
            obj.modified_date = date_time
            obj.save()
        super(BlogAdmin, self).save_model(request, obj, form, change)
        return


admin.site.register(Blog, BlogAdmin)