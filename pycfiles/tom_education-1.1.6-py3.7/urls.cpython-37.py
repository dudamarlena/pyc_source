# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/urls.py
# Compiled at: 2020-04-30 08:35:11
# Size of source mod 2**32: 1735 bytes
from django.urls import path
from tom_targets.views import TargetDetailView
from tom_education.views import ActionableTargetDetailView, AsyncStatusApi, DataProductDeleteMultipleView, EducationTargetCreateView, EducationTargetUpdateView, GalleryView, ObservationAlertApiCreateView, PipelineProcessApi, PipelineProcessDetailView, TemplatedObservationCreateView, TargetDetailApiView, photometry_to_csv
app_name = 'tom_education'
urlpatterns = [
 path('observations/<str:facility>/create/', (TemplatedObservationCreateView.as_view()), name='create_obs'),
 path('targets/<int:pk>/', (TargetDetailView.as_view()), name='target_detail'),
 path('targets/create/', (EducationTargetCreateView.as_view()), name='target_create'),
 path('targets/<pk>/update/', (EducationTargetUpdateView.as_view()), name='target_update'),
 path('targets/<int:pk>/data/', (ActionableTargetDetailView.as_view()), name='target_data'),
 path('targets/<int:pk>/data/download/', photometry_to_csv, name='photometry_download'),
 path('pipeline/<pk>', (PipelineProcessDetailView.as_view()), name='pipeline_detail'),
 path('gallery/', (GalleryView.as_view()), name='gallery'),
 path('dataproducts/deletemultiple/', (DataProductDeleteMultipleView.as_view()), name='delete_dataproducts'),
 path('api/async/status/<target>/', (AsyncStatusApi.as_view()), name='async_process_status_api'),
 path('api/pipeline/logs/<pk>/', (PipelineProcessApi.as_view()), name='pipeline_api'),
 path('api/target/<pk>/', (TargetDetailApiView.as_view()), name='target_api'),
 path('api/observe/', (ObservationAlertApiCreateView.as_view()), name='observe_api')]