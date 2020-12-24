# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/urls.py
# Compiled at: 2016-09-28 11:51:43
from . import views

def register_in(router):
    router.register('sugarcrm', views.SugarCRMServiceViewSet, base_name='sugarcrm')
    router.register('sugarcrm-crms', views.CRMViewSet, base_name='sugarcrm-crms')
    router.register('sugarcrm-service-project-link', views.SugarCRMServiceProjectLinkViewSet, base_name='sugarcrm-spl')
    router.register('sugarcrm-crms/(?P<crm_uuid>[\\w]+)/users', views.CRMUserViewSet, base_name='sugarcrm-users')