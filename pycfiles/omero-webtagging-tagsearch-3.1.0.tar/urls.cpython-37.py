# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpwrussell/Checkout/OME/webtagging/tagsearch/omero_webtagging_tagsearch/urls.py
# Compiled at: 2020-01-12 13:54:38
# Size of source mod 2**32: 275 bytes
from django.conf.urls import url
from . import views
urlpatterns = [
 url('^$', (views.index), name='tagsearch'),
 url('^images$', (views.tag_image_search), name='wtsimages')]