# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tigorc/repo/django-redactorjs/redactor/urls.py
# Compiled at: 2016-08-30 10:29:24
# Size of source mod 2**32: 531 bytes
try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url, patterns

from redactor.views import DefaultRedactorUploadView
from redactor.forms import FileForm
urlpatterns = [
 url('^upload/image/(?P<upload_to>.*)', DefaultRedactorUploadView.as_view(), name='redactor_upload_image'),
 url('^upload/file/(?P<upload_to>.*)', DefaultRedactorUploadView.as_view(), {'form_class': FileForm}, name='redactor_upload_file')]