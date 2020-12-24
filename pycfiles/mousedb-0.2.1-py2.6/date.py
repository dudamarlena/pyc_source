# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/animal/urls/date.py
# Compiled at: 2010-08-13 20:24:02
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.date_based import archive_year, archive_month
from mousedb.animal.models import Animal

@login_required
def limited_archive_year(*args, **kwargs):
    return archive_year(*args, **kwargs)


@login_required
def limited_archive_month(*args, **kwargs):
    return archive_month(*args, **kwargs)


urlpatterns = patterns('', ('^$', 'mousedb.views.home'), (
 '^(?P<year>\\d{4})/$', limited_archive_year,
 {'queryset': Animal.objects.all(), 
    'date_field': 'Born', 
    'template_name': 'animal_list.html', 
    'template_object_name': 'animal', 
    'make_object_list': True}), (
 '^(?P<year>\\d{4})/(?P<month>\\d{2})/$', limited_archive_month,
 {'queryset': Animal.objects.all(), 
    'date_field': 'Born', 
    'month_format': '%m', 
    'template_name': 'animal_list.html', 
    'template_object_name': 'animal'}))