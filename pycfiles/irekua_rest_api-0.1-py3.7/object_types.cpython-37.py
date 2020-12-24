# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/urls/object_types.py
# Compiled at: 2019-10-28 01:57:31
# Size of source mod 2**32: 2170 bytes
from rest_framework import routers
from irekua_rest_api import views
object_types_router = routers.DefaultRouter()
object_types_router.register('mime_types', views.MimeTypeViewSet)
object_types_router.register('annotation_types', views.AnnotationTypeViewSet)
object_types_router.register('collection_types', views.CollectionTypeViewSet)
object_types_router.register('device_types', views.DeviceTypeViewSet)
object_types_router.register('entailment_types', views.EntailmentTypeViewSet)
object_types_router.register('event_types', views.EventTypeViewSet)
object_types_router.register('item_types', views.ItemTypeViewSet)
object_types_router.register('licence_types', views.LicenceTypeViewSet)
object_types_router.register('sampling_event_type_device_types', views.SamplingEventTypeDeviceTypeViewSet)
object_types_router.register('sampling_event_type_site_types', views.SamplingEventTypeSiteTypeViewSet)
object_types_router.register('sampling_event_types', views.SamplingEventTypeViewSet)
object_types_router.register('site_types', views.SiteTypeViewSet)
object_types_router.register('collection_type_site_types', views.CollectionTypeSiteTypeViewSet)
object_types_router.register('collection_type_administrators', views.CollectionTypeAdministratorViewSet)
object_types_router.register('collection_type_annotation_types', views.CollectionTypeAnnotationTypeViewSet)
object_types_router.register('collection_type_licence_types', views.CollectionTypeLicenceTypeViewSet)
object_types_router.register('collection_type_sampling_event_types', views.CollectionTypeSamplingEventTypeViewSet)
object_types_router.register('collection_type_item_types', views.CollectionTypeItemTypeViewSet)
object_types_router.register('collection_type_event_types', views.CollectionTypeEventTypeViewSet)
object_types_router.register('collection_type_device_types', views.CollectionTypeDeviceTypeViewSet)
object_types_router.register('collection_type_roles', views.CollectionTypeRoleViewSet)