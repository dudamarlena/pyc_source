# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/glyphviewer/urls.py
# Compiled at: 2018-03-17 21:18:09
from django.conf.urls import url, include
from views import index as glyphindex, doc as glyphdoc
urlpatterns = [
 url('^$', glyphindex), url('^doc/$', glyphdoc)]