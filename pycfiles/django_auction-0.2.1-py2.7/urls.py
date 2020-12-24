# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/auction/urls.py
# Compiled at: 2013-04-22 04:27:13
from django.conf.urls.defaults import patterns, include, url
import auction.views
urlpatterns = patterns('', url('^$', auction.views.AuctionListView.as_view(), name='auctions'), url('^bids/$', auction.views.BidListView.as_view(), name='bids'), url('^bids/delete/(?P<bid_id>\\d+)/$', auction.views.BidDetailView.as_view(action='delete'), name='delete_bid'), url('^auction/(?P<slug>[0-9A-Za-z-_.]+)/$', auction.views.AuctionView.as_view(), name='auction'), url('^auction/(?P<auction_slug>[0-9A-Za-z-_.]+)/lot/(?P<slug>[0-9A-Za-z-_.//]+)/(?P<pk>\\d+)/$', auction.views.LotDetailView.as_view(), name='lot'))