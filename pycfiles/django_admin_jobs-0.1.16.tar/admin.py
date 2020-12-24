# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\dipap\Desktop\Projects\Orfium\project\earnings-dashboard\upload_tools\admin.py
# Compiled at: 2017-12-07 10:19:14
from __future__ import unicode_literals
from django.utils.safestring import mark_safe
from .models import *
from django.contrib import admin

class UploadJobAdmin(admin.ModelAdmin):
    list_display = ('code', 'created', 'start_time', 'end_time', 'status', 'details')
    list_filter = ('status', )
    readonly_fields = ('id', 'started', 'finished', 'status', 'info', 'upload_type')
    change_list_template = b'admin/upload_tools/upload_job/change_list.html'
    actions = [
     b'restart_action']

    def restart_action(self, request, queryset):
        cnt = queryset.count()
        for job in queryset:
            job.restart()

        self.message_user(request, b'%s job(s) restarted.' % cnt)

    restart_action.short_description = b'Restart selected job(s)'

    def start_time(self, obj):
        if obj.started:
            return obj.started.strftime(b'%Y-%m-%d %H:%M:%S')
        return b'-'

    def end_time(self, obj):
        if obj.finished:
            return obj.finished.strftime(b'%Y-%m-%d %H:%M:%S')
        return b'-'

    def code(self, obj):
        return mark_safe(b'<div class="upload-job-code%s" data-jobid="%s">%s</div>' % (
         b' finished' if obj.status == b'FINISHED' else b'', str(obj.pk), str(obj.pk)[:6]))

    def details(self, obj):
        return obj.info


class AssetUploadJobAdmin(UploadJobAdmin):
    pass


admin.site.register(AssetUploadJob, AssetUploadJobAdmin)