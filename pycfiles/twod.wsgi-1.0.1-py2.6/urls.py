# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/fixtures/sampledjango/urls.py
# Compiled at: 2011-06-28 10:17:42
from django.conf.urls.defaults import *
from tests.fixtures.sampledjango.app1 import urls as app1_urls
from tests.fixtures.sampledjango.app2 import urls as app2_urls
urlpatterns = patterns('', (
 '^app1/', include(app1_urls)), (
 '^app2/', include(app2_urls)))