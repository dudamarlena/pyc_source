# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /django/.envs/simpletickets/local/lib/python2.7/site-packages/simpletickets/urls.py
# Compiled at: 2016-09-24 08:06:11
from django.conf.urls import url
from django.contrib import admin
from .views import TicketList, TicketCreate, TicketDelete, TicketUpdate
from simpletickets.settings.ticketSettings import ST_REST_API, API_BASE_URL
from .api.views import UserTicketListCreate, UserTicketUpdateDelete, StaffTicketList, StaffTicketUpdate
admin.autodiscover()
urlpatterns = [
 url('^list/$', TicketList.as_view(), name='ticketList'),
 url('^new-ticket/$', TicketCreate.as_view(), name='newTicket'),
 url('^edit-ticket-(?P<ST_id>[\\d]*)/$', TicketUpdate.as_view(), name='TicketUpdate'),
 url('^delete-ticket-(?P<ST_id>[\\d]*)/$', TicketDelete.as_view(), name='TicketDelete')]
if ST_REST_API:
    urlpatterns += [
     url(('^{url}/list-create/$').format(url=API_BASE_URL), UserTicketListCreate.as_view(), name='apiListCreate'),
     url(('^{url}/ticket-(?P<pk>[\\d]+)-update-destroy/$').format(url=API_BASE_URL), UserTicketUpdateDelete.as_view(), name='updateDestroyCreate'),
     url(('^{url}/staff-list/$').format(url=API_BASE_URL), StaffTicketList.as_view(), name='apiListCreate'),
     url(('^{url}/staff-ticket-(?P<pk>[\\d]+)-update/$').format(url=API_BASE_URL), StaffTicketUpdate.as_view(), name='updateDestroyCreate')]