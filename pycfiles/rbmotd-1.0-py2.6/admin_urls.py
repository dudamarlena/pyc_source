# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/rbmotd/admin_urls.py
# Compiled at: 2014-06-24 00:16:14
from django.conf.urls import patterns
from rbmotd.extension import MotdExtension
from rbmotd.forms import MotdSettingsForm
urlpatterns = patterns('', (
 '^$', 'reviewboard.extensions.views.configure_extension',
 {'ext_class': MotdExtension, 
    'form_class': MotdSettingsForm}))