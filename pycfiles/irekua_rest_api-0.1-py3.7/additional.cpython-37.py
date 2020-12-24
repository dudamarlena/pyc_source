# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/urls/additional.py
# Compiled at: 2019-10-28 01:57:36
# Size of source mod 2**32: 1763 bytes
from rest_framework import routers
from irekua_rest_api import views
additional_router = routers.DefaultRouter()
additional_router.register('annotation_votes', views.AnnotationVoteViewSet)
additional_router.register('secondary_items', views.SecondaryItemViewSet)
additional_router.register('annotation_tools', views.AnnotationToolViewSet)
additional_router.register('collection_devices', views.CollectionDeviceViewSet)
additional_router.register('collection_sites', views.CollectionSiteViewSet)
additional_router.register('collection_users', views.CollectionUserViewSet)
additional_router.register('collection_administrators', views.CollectionAdministratorViewSet)
additional_router.register('device_brands', views.DeviceBrandViewSet)
additional_router.register('entailments', views.EntailmentViewSet)
additional_router.register('institutions', views.InstitutionViewSet)
additional_router.register('licences', views.LicenceViewSet)
additional_router.register('metacollections', views.MetaCollectionViewSet)
additional_router.register('physical_devices', views.PhysicalDeviceViewSet)
additional_router.register('roles', views.RoleViewSet)
additional_router.register('synonym_suggestions', views.SynonymSuggestionViewSet)
additional_router.register('synonyms', views.SynonymViewSet)
additional_router.register('tags', views.TagViewSet)
additional_router.register('term_suggestions', views.TermSuggestionViewSet)
additional_router.register('term_instances', views.TermViewSet)
additional_router.register('sampling_event_devices', views.SamplingEventDeviceViewSet)