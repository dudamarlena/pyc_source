# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tigorc/repo/django-redactorjs/redactor/urls.py
# Compiled at: 2015-10-18 11:02:31
try:
    from django.conf.urls import url, patterns
except ImportError:
    from django.conf.urls.defaults import url, patterns

from redactor.views import DefaultRedactorUploadView
from redactor.forms import FileForm
urlpatterns = patterns('', url('^upload/image/(?P<upload_to>.*)', DefaultRedactorUploadView.as_view(), name='redactor_upload_image'), url('^upload/file/(?P<upload_to>.*)', DefaultRedactorUploadView.as_view(), {'form_class': FileForm}, name='redactor_upload_file'))