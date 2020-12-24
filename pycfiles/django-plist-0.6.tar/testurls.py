# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/steingrd/Django/django-plist/django_plist/tests/testurls.py
# Compiled at: 2010-05-19 01:29:02
from django.conf.urls.defaults import *
from testapp.models import Author, Blog
urlpatterns = patterns('', (
 '^blogs_noempty/$', 'django_plist.views.generic.plist_array', {'queryset': Blog.objects.all(), 'allow_empty': False}), (
 '^blogs_allowempty/$', 'django_plist.views.generic.plist_array', {'queryset': Blog.objects.all(), 'allow_empty': True}), (
 '^authors_allowempty/$', 'django_plist.views.generic.plist_array', {'queryset': Author.objects.all(), 'allow_empty': True}))