# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_organization/urls.py
# Compiled at: 2016-09-25 10:50:25
from __future__ import unicode_literals
from nodeconductor_organization import views

def register_in(router):
    router.register(b'organizations', views.OrganizationViewSet, base_name=b'organization')
    router.register(b'organization-users', views.OrganizationUserViewSet, base_name=b'organization_user')