# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_auth_valimo/urls.py
# Compiled at: 2016-09-19 07:37:17
from __future__ import unicode_literals
from . import views

def register_in(router):
    router.register(b'auth-valimo', views.AuthResultViewSet, base_name=b'auth-valimo')