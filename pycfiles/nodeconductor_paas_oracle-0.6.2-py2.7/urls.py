# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_paas_oracle/urls.py
# Compiled at: 2016-12-16 07:39:01
from . import views

def register_in(router):
    router.register('oracle', views.OracleServiceViewSet, base_name='oracle')
    router.register('oracle-service-project-link', views.OracleServiceProjectLinkViewSet, base_name='oracle-spl')
    router.register('oracle-deployments', views.DeploymentViewSet, base_name='oracle-deployments')
    router.register('oracle-flavors', views.FlavorViewSet, base_name='oracle-flavors')