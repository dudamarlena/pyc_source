# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hgwebproxy/urls.py
# Compiled at: 2009-07-31 16:05:31
from django.conf.urls.defaults import *
urlpatterns = patterns('hgwebproxy.views', url('^$', 'repo_list', name='repo_list'), url('^(?P<slug>[\\w-]+)/', 'repo', name='repo_detail'))