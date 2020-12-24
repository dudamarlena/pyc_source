# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/videos/admin.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 3253 bytes
from django.contrib import admin
import django.utils.translation as _
from tendenci.apps.perms.admin import TendenciBaseModelAdmin
from tendenci.apps.videos.models import Video, Category, VideoType
from tendenci.apps.videos.forms import VideoForm
from tendenci.apps.site_settings.utils import get_setting
import tendenci.apps.theme.templatetags.static as static

class VideoInline(admin.TabularInline):
    model = Video
    max_num = 0
    can_delete = False
    fields = ('title', 'tags')
    readonly_fields = ('title', 'tags')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position')
    list_editable = ['position', 'name']
    prepopulated_fields = {'slug': ['name']}
    inlines = [VideoInline]
    ordering = ('position', )

    class Media:
        js = (
         '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
         '//ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',
         static('js/admin/admin-list-reorder.js'))


class VideoTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    prepopulated_fields = {'slug': ['name']}


class VideoAdmin(TendenciBaseModelAdmin):

    def get_release_dt(self, instance):
        dt = instance.release_dt
        if dt:
            return dt.strftime('%x')
        return ''

    get_release_dt.short_description = _('Release Date')
    list_display = ['title', 'tags', 'category', 'video_type', 'get_release_dt']
    list_editable = ['category', 'video_type']
    if not get_setting('module', 'videos', 'order_by_release_dt'):
        list_display.append('position')
        list_editable.append('position')
    else:
        prepopulated_fields = {'slug': ['title']}
        search_fields = ['title', 'description']
        fieldsets = (
         (
          None, {'fields': ('title', 'slug', 'category', 'video_type', 'image', 'clear_image', 'video_url', 'tags',
 'description', 'release_dt')}),
         (
          'Permissions', {'fields': ('allow_anonymous_view', )}),
         (
          'Advanced Permissions',
          {'classes':('collapse', ),  'fields':('user_perms', 'member_perms', 'group_perms')}),
         (
          'Publishing Status',
          {'fields': ('status_detail', )}))
        form = VideoForm
        if not get_setting('module', 'videos', 'order_by_release_dt'):
            ordering = [
             '-position']
        else:
            ordering = [
             '-release_dt']

    class Media:
        js = (
         '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
         '//ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',
         static('js/admin/admin-list-reorder.js'),
         static('js/global/tinymce.event_handlers.js'))

    def get_fieldsets--- This code section failed: ---

 L.  81         0  LOAD_GLOBAL              super
                2  LOAD_GLOBAL              VideoAdmin
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  LOAD_METHOD              get_fieldsets
               10  LOAD_FAST                'request'
               12  LOAD_FAST                'obj'
               14  CALL_METHOD_2         2  '2 positional arguments'
               16  STORE_FAST               'fieldsets'

 L.  82        18  LOAD_FAST                'obj'
               20  POP_JUMP_IF_FALSE    32  'to 32'
               22  LOAD_FAST                'obj'
               24  POP_JUMP_IF_FALSE    90  'to 90'
               26  LOAD_FAST                'obj'
               28  LOAD_ATTR                image
               30  POP_JUMP_IF_TRUE     90  'to 90'
             32_0  COME_FROM            20  '20'

 L.  83        32  LOAD_GLOBAL              list
               34  LOAD_FAST                'fieldsets'
               36  LOAD_CONST               0
               38  BINARY_SUBSCR    
               40  LOAD_CONST               1
               42  BINARY_SUBSCR    
               44  LOAD_STR                 'fields'
               46  BINARY_SUBSCR    
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  STORE_FAST               'fields'

 L.  84        52  LOAD_STR                 'clear_image'
               54  LOAD_FAST                'fields'
               56  COMPARE_OP               in
               58  POP_JUMP_IF_FALSE    90  'to 90'

 L.  85        60  LOAD_FAST                'fields'
               62  LOAD_METHOD              remove
               64  LOAD_STR                 'clear_image'
               66  CALL_METHOD_1         1  '1 positional argument'
               68  POP_TOP          

 L.  86        70  LOAD_GLOBAL              tuple
               72  LOAD_FAST                'fields'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  LOAD_FAST                'fieldsets'
               78  LOAD_CONST               0
               80  BINARY_SUBSCR    
               82  LOAD_CONST               1
               84  BINARY_SUBSCR    
               86  LOAD_STR                 'fields'
               88  STORE_SUBSCR     
             90_0  COME_FROM            58  '58'
             90_1  COME_FROM            30  '30'
             90_2  COME_FROM            24  '24'

 L.  87        90  LOAD_FAST                'fieldsets'
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 92


admin.site.register(Video, VideoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(VideoType, VideoTypeAdmin)