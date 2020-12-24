# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/urls.py
# Compiled at: 2016-09-28 02:05:53
from . import views

def register_in(router):
    router.register('sharepoint-templates', views.TemplateViewSet, base_name='sharepoint-templates')
    router.register('sharepoint-tenants', views.TenantViewSet, base_name='sharepoint-tenants')
    router.register('sharepoint-users', views.UserViewSet, base_name='sharepoint-users')
    router.register('sharepoint-site-collections', views.SiteCollectionViewSet, base_name='sharepoint-site-collections')