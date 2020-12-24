# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yuji/Projects/Stimson/stimson_project/env/lib/python2.7/site-packages/cleditor/admin.py
# Compiled at: 2012-01-25 21:01:14
import os
from django import http
from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import patterns
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt

class CLEditorUploadAdmin(admin.ModelAdmin):
    upload_to = 'cleditoruploads/'

    def get_urls(self):
        urls = super(CLEditorUploadAdmin, self).get_urls()
        my_urls = patterns('', (
         'upload-image/$', self.admin_site.admin_view(self.upload_handler)))
        return my_urls + urls

    @csrf_exempt
    def upload_handler(self, request):
        """
                Handle widget uploader
                """
        if not request.POST:
            raise http.Http404
        f = request.FILES['imageName']
        result = default_storage.save(os.path.join(self.upload_to, f.name), f)
        return http.HttpResponse(('<div id="image">{static_url}{path}</div>').format(static_url=settings.STATIC_URL, path=result))