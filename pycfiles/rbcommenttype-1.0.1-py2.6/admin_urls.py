# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/rbcommenttype/admin_urls.py
# Compiled at: 2015-12-14 18:14:24
from __future__ import unicode_literals
from django.conf.urls import patterns, url
from rbcommenttype.extension import CommentTypeExtension
from rbcommenttype.forms import CommentTypeSettingsForm
urlpatterns = patterns(b'', url(b'^$', b'reviewboard.extensions.views.configure_extension', {b'ext_class': CommentTypeExtension, 
   b'form_class': CommentTypeSettingsForm}, name=b'rbcommenttype-configure'))