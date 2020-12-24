# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/django_propeller_demo/urls.py
# Compiled at: 2017-03-24 13:36:01
from __future__ import unicode_literals
from django.conf.urls import url
from .views import HomePageView, FormHorizontalView, FormInlineView, PaginationView, FormWithFilesView, DefaultFormView, MiscView, DefaultFormsetView, DefaultFormByFieldView, ButtonsView, FABsView, TypoView, NavBarView, CardView
urlpatterns = [
 url(b'^$', HomePageView.as_view(), name=b'home'),
 url(b'^typo$', TypoView.as_view(), name=b'typo'),
 url(b'^buttons$', ButtonsView.as_view(), name=b'buttons'),
 url(b'^fabs$', FABsView.as_view(), name=b'fabs'),
 url(b'^navbar$', NavBarView.as_view(), name=b'navbar'),
 url(b'^cards$', CardView.as_view(), name=b'cards'),
 url(b'^formset$', DefaultFormsetView.as_view(), name=b'formset_default'),
 url(b'^form$', DefaultFormView.as_view(), name=b'form_default'),
 url(b'^form_by_field$', DefaultFormByFieldView.as_view(), name=b'form_by_field'),
 url(b'^form_horizontal$', FormHorizontalView.as_view(), name=b'form_horizontal'),
 url(b'^form_inline$', FormInlineView.as_view(), name=b'form_inline'),
 url(b'^form_with_files$', FormWithFilesView.as_view(), name=b'form_with_files'),
 url(b'^pagination$', PaginationView.as_view(), name=b'pagination'),
 url(b'^misc$', MiscView.as_view(), name=b'misc')]