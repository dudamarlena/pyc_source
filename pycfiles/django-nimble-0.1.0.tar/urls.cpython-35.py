# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\Django\development\nimble\urls.py
# Compiled at: 2017-01-30 17:02:42
# Size of source mod 2**32: 1588 bytes
from django.conf.urls import include, url
from rest_framework import routers
from .serializers.debt import DebtViewSet
from .serializers.feature import FeatureViewSet
from .serializers.profile import ProfileViewSet
from .serializers.user import UserViewSet
from .views.control_panel import ControlPanelView
from .views.dashboard import DashboardView
from .views.story_create import StoryCreate
from .views.story_detail import StoryDetail
from .views.story_history import StoryHistory
from .views.story_list import StoryList
router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('profiles', ProfileViewSet)
router.register('debts', DebtViewSet)
router.register('features', FeatureViewSet)
urlpatterns = [
 url('^$', DashboardView.as_view(), name='dashboard'),
 url('^control_panel/$', ControlPanelView.as_view(), name='control_panel'),
 url('^api/', include(router.urls), name='rootapi'),
 url('^api-auth/', include('rest_framework.urls')),
 url('^stories/$', StoryList.as_view(), name='stories'),
 url('^(?P<ident>D|F)(?P<pk>[0-9]+)/$', StoryDetail.as_view(), name='story_detail'),
 url('^new/(?P<story_type>debt|feature)/$', StoryCreate.as_view(), name='story_create'),
 url('^(?P<ident>D|F)(?P<pk>[0-9]+)/history/$', StoryHistory.as_view(), name='story_history')]