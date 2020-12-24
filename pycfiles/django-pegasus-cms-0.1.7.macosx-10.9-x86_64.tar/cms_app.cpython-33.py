# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/apps/search/cms_app.py
# Compiled at: 2015-02-18 15:30:56
# Size of source mod 2**32: 605 bytes
from __future__ import absolute_import, division
from cms.apphook_pool import apphook_pool
from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from .views import CeleritySearchView
from cms.app_base import CMSApp

class SearchApphook(CMSApp):
    name = _('Search')
    urls = [
     patterns('', url('^$', CeleritySearchView.as_view(), name='celerity-search'))]


apphook_pool.register(SearchApphook)