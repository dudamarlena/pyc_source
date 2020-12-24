# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simple_autocomplete/urls.py
# Compiled at: 2016-11-08 09:30:37
from django.conf.urls import url
from simple_autocomplete.views import get_json
urlpatterns = [
 url('^(?P<token>[\\w-]+)/$', get_json, name='simple-autocomplete')]