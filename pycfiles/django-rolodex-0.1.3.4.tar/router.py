# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jon/DMN/Scripts/django-rolodex/rolodex/API/router.py
# Compiled at: 2016-01-21 13:59:18
from rest_framework import routers
from rolodex.API import views
router = routers.DefaultRouter()
router.register('roles', views.RoleViewSet)
router.register('contact-roles', views.ContactRoleViewSet)
router.register('contacts', views.ContactViewSet)
router.register('people', views.PersonViewSet)
router.register('orgs', views.OrgViewSet)
router.register('relationships/person_to_person', views.P2PViewSet)
router.register('relationships/org_to_org', views.Org2OrgViewSet)
router.register('relationships/org_to_person', views.Org2PViewSet)
router.register('relationships/person_to_org', views.P2OrgViewSet)
router.register('relationships/types/person_to_person', views.P2P_TypeViewSet)
router.register('relationships/types/org_to_org', views.Org2Org_TypeViewSet)
router.register('relationships/types/person_to_org', views.P2Org_TypeViewSet)