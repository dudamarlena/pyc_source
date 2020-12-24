# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/demo/urls.py
# Compiled at: 2017-02-17 12:55:03
# Size of source mod 2**32: 947 bytes
from __future__ import unicode_literals
from django.conf.urls import url
from .views import HomePageView, FormHorizontalView, FormInlineView, PaginationView, FormWithFilesView, DefaultFormView, MiscView, DefaultFormsetView, DefaultFormByFieldView
urlpatterns = [
 url('^$', HomePageView.as_view(), name='home'),
 url('^formset$', DefaultFormsetView.as_view(), name='formset_default'),
 url('^form$', DefaultFormView.as_view(), name='form_default'),
 url('^form_by_field$', DefaultFormByFieldView.as_view(), name='form_by_field'),
 url('^form_horizontal$', FormHorizontalView.as_view(), name='form_horizontal'),
 url('^form_inline$', FormInlineView.as_view(), name='form_inline'),
 url('^form_with_files$', FormWithFilesView.as_view(), name='form_with_files'),
 url('^pagination$', PaginationView.as_view(), name='pagination'),
 url('^misc$', MiscView.as_view(), name='misc')]