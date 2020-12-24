# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dpl1_main/testing_app/url_util.py
# Compiled at: 2014-02-18 08:16:00
from django.conf.urls import url
from views import pages_view
test_pages_url = url('^tests/(?P<test_id>\\d+)/(?P<page_id>\\d+)', pages_view, name='pages')