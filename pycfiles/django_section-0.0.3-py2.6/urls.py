# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/section/tests/urls.py
# Compiled at: 2011-08-24 05:29:23
from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('', url('some/url', 'section.tests.views.view', name='unmatched_section'), url('some/other/url', 'section.tests.views.view', name='matched_section'), url('some/other/matching/url', 'section.tests.views.view', name='matched_section_with_second_path'))