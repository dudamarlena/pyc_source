# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andretavares/Dev/AptanaStudio3Workspace/restauranteur/yplaces/api/urls.py
# Compiled at: 2014-02-24 13:15:56
from django.conf.urls import patterns, url
from handlers import PlacesHandler, PlaceIdHandler, ReviewsHandler, ReviewIdHandler, PhotosHandler, PhotoIdHandler
urlpatterns = patterns('', url('^/?$', PlacesHandler.as_view(), name='index'), url('^/(?P<pk>[0-9]+)/?$', PlaceIdHandler.as_view(), name='id'), url('^/(?P<pk>[0-9]+)/photos/?$', PhotosHandler.as_view(), name='photos'), url('^/(?P<pk>[0-9]+)/photos/(?P<photo_pk>[0-9]+)/?$', PhotoIdHandler.as_view(), name='photo_id'), url('^/(?P<pk>[0-9]+)/reviews/?$', ReviewsHandler.as_view(), name='reviews'), url('^/(?P<pk>[0-9]+)/reviews/(?P<review_pk>[0-9]+)/?$', ReviewIdHandler.as_view(), name='review_id'))