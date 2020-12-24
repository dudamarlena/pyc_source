# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/metaimage/admin.py
# Compiled at: 2011-05-09 23:35:04
from django.contrib import admin
from metaimage.models import MetaImage

class BaseModelAdmin(admin.ModelAdmin):
    """
    Because the sage.models relies on the BaseModel abstract class,
    Django's admin UI does not automagically pick up the
    BaseModel.creator and BaseModel.updater fields; in particular, the
    creator field is required.  So create an inheritable save_model()
    method that takes care of that.
    """

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        else:
            obj.updater = request.user
        obj.save()


class MetaImageAdmin(BaseModelAdmin):
    fieldsets = (
     (
      None,
      {'fields': ('image', 'crop_from', 'effect', 'title', 'slug', 'caption', 'source_url', 'source_note',
 'safetylevel', 'privacy', 'tags', 'imageset', 'admin_notes', 'is_active')}),)
    list_display = ('title', 'slug', 'caption', 'creator', 'created', 'is_public',
                    'safetylevel', 'the_tags')
    prepopulated_fields = {'slug': ('title', )}

    def the_tags(self, obj):
        """
        This workaround of m2m limitation of django-taggit is from
        https://github.com/alex/django-taggit/issues/46
        """
        return '%s' % (obj.tags.all(),)

    the_tags.short_description = 'Tags'


admin.site.register(MetaImage, MetaImageAdmin)