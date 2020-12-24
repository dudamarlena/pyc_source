# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/skylar/pinax/projects/NASA/apps/listings/urls.py
# Compiled at: 2009-08-18 07:43:08
from django.conf.urls.defaults import *
urlpatterns = patterns('', url('^$', 'listings.views.listings', name='listings_all'), url('^(?P<id>\\d+)/(?P<slug>[-\\w]+)/$', 'listings.views.listing', name='listings_detail'), url('^your_listings/$', 'listings.views.your_listings', name='listings_yours'), url('watched_listings/$', 'listings.views.watched_listings', name='listings_watched'), url('^create/$', 'listings.views.new', name='listings_new'), url('^edit/(?P<listing_id>\\d+)/$', 'listings.views.edit_listing', name='listings_edit'), url('^delete/(?P<listing_id>\\d+)/$', 'listings.views.delete_listing', name='listings_delete'), url('^watch/(?P<listing_id>\\d+)/$', 'listings.views.watch', name='listings_watch'))