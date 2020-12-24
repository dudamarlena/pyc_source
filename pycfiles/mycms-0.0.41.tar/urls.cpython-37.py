# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/urls.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 3008 bytes
from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt
from mycms.views import CMSContentsAPIView, CMSEntriesAPIView, CMSMarkUpsAPIView, CMSTemplatesAPIView, CMSPageView, CMSPathsAPIView, CMSEntriesROAPIView, LoremIpsumAPIView, AssetsUploaderView, CMSPageTypesAPIView, CMSFileUpload
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
import rest_framework.authtoken as authtoken_views
from mycms.views import TemplateSampleLoader
from mycms.views import CMSUserContentArea
from rest_framework import routers
from mycms import api
from mycms.views import CMSFormatterContent
urlpatterns = [
 url('^search/', include('haystack.urls')),
 url('^(?P<path>[-/\\.a-z\\d_]*)/assets_manager/$', (csrf_exempt(AssetsUploaderView.as_view())), name='assets_manager_get'),
 url('^(?P<path>[-/\\.a-z\\d_]*)/assets_manager/(?P<filename>[-/\\.a-z\\d_A-Z]*)$', (csrf_exempt(AssetsUploaderView.as_view())), name='assets_manager_get'),
 url('^templates/(?P<template>[-._\\w\\W\\d]*.html)$', TemplateSampleLoader.as_view()),
 url('^templates/?$', TemplateSampleLoader.as_view()),
 url('^user/admin/articles/?$', CMSUserContentArea.as_view()),
 url('^(?P<path>[-/\\.a-z\\d_]*)/$', (CMSPageView.as_view()), name='cms_page'),
 url('^$', (CMSPageView.as_view()), name='cms_page')]
schema_view = get_schema_view(title='MyCMS API')
cms_root = [
 url('^$', (CMSPageView.as_view()), name='cms_page'),
 url('^api/v2/docs/', include_docs_urls(title='MyCMS API')),
 url('^api/v2/schemas/', schema_view),
 url('api/v2/cmsauthtoken', (api.CMSAuthToken.as_view({'post': 'retrieve'})), name='cmsauthtoken'),
 url('api/v2/cmspreview', (api.CMSContentPreview.as_view({'post': 'retrieve'})), name='cmspreview')]
router = routers.DefaultRouter()
router.register('api/v2/cmscontents', (api.CMSContentsViewSet), base_name='cmscontents')
router.register('api/v2/cmsentries', (api.CMSEntriesViewSet), base_name='cmsentries')
router.register('api/v2/cmspaths', (api.CMSPathsViewSet), base_name='cmspaths')
router.register('api/v2/cmspages', (api.CMSPagesViewSet), base_name='cmspages')
urlpatterns = cms_root + router.urls + urlpatterns