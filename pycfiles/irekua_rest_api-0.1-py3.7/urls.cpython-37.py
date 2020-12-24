# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/project/urls.py
# Compiled at: 2019-10-31 17:50:13
# Size of source mod 2**32: 142 bytes
from django.conf.urls import url
from django.conf.urls import include
urlpatterns = [
 url('^api/', include('irekua_rest_api.urls'))]