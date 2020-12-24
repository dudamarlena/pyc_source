# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ivan/pycharm-workplace/test_ftp/pureftpd_admin/urls.py
# Compiled at: 2014-11-04 09:11:54
from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
__author__ = 'ivan'
from pureftpd_admin.localdir.views import serve
import ftpusers.settings as ftpusets_settings
urlpatterns = patterns('', url('^localdir/(?P<path>.*)$', staff_member_required(serve), kwargs={'document_root': ftpusets_settings.ROOT_PATH}, name='localdir-ftpusers-url'))