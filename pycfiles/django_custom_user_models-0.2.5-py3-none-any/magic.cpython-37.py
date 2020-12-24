# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\urls\magic.py
# Compiled at: 2020-01-28 13:32:35
# Size of source mod 2**32: 215 bytes
from django.conf.urls import url
from CustomAuth.views import login
urlpatterns = [
 url('(?P<magic_uid64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', login, name='magic login')]