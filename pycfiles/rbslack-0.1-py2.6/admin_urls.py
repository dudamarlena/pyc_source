# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/rbslack/admin_urls.py
# Compiled at: 2016-03-05 05:42:36
from __future__ import unicode_literals
from django.conf.urls import patterns
from rbslack.extension import SlackExtension
from rbslack.forms import SlackSettingsForm
urlpatterns = patterns(b'', (
 b'^$', b'reviewboard.extensions.views.configure_extension',
 {b'ext_class': SlackExtension, 
    b'form_class': SlackSettingsForm}))