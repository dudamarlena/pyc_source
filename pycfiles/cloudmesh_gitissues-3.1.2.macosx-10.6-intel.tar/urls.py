# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/big/ENV2/lib/python2.7/site-packages/cloudmesh_gitissues/urls.py
# Compiled at: 2016-03-16 12:51:25
"""comet URL Configuration

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.contrib import admin
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .views import homepage
from .issues.views import issue_list, issue_list_html5

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register('users', UserViewSet)
urlpatterns = [
 url('^sitemap\\.xml$', sitemap, {'sitemaps': {'flatpages': FlatPageSitemap}}, name='django.contrib.sitemaps.views.sitemap'),
 url('^admin/', include(admin.site.urls)),
 url('^docs/', include('rest_framework_swagger.urls')),
 url('^pages/', include('django.contrib.flatpages.urls')),
 url('^$', homepage, name='home'),
 url('^issues/list/$', issue_list, name='issue_list'),
 url('^issues/list/(?P<username>\\w+)/(?P<repository>[-\\w]+)/$', issue_list, name='issue_list'),
 url('^', include(router.urls)),
 url('^api-auth/', include('rest_framework.urls', namespace='rest_framework'))]