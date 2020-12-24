# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/Aptana_Studio_Workspace/mp_test/mixpanel_django/example/mp_example/urls.py
# Compiled at: 2010-12-17 03:51:33
from django.conf.urls.defaults import *
urlpatterns = patterns('mp_example', ('^$', 'views.test_mp_view'))