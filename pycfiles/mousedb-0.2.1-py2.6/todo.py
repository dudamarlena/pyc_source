# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/animal/urls/todo.py
# Compiled at: 2010-08-13 20:24:02
"""URL configuration file for todo subpages.

This controls any page /mousedb/todo/ and sends it to the appropriate views."""
import datetime
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required
from mousedb.animal.models import Animal

@login_required
def limited_object_list(*args, **kwargs):
    return object_list(*args, **kwargs)


@login_required
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)


wean = datetime.date.today() - datetime.timedelta(days=30)
urlpatterns = patterns('', url('^$', 'mousedb.views.todo', name='todo-list'), url('^eartag/$', limited_object_list, {'queryset': Animal.objects.filter(MouseID__isnull=True, Alive=True), 
   'template_name': 'animal_list.html', 
   'template_object_name': 'animal'}, name='todo-eartags'), url('^genotype/$', limited_object_list, {'queryset': Animal.objects.filter(Genotype='N.D.', Alive=True).exclude(Strain__Strain='C57BL/6'), 
   'template_name': 'animal_list.html', 
   'template_object_name': 'animal'}, name='todo-genotype'), url('^wean/$', limited_object_list, {'queryset': Animal.objects.filter(Born__gt=wean).filter(Weaned=None, Alive=True).exclude(Strain=2), 
   'template_name': 'animal_list.html', 
   'template_object_name': 'animal'}, name='todo-weaning'), url('^no_cage/$', limited_object_list, {'queryset': Animal.objects.filter(Cage__exact=None).filter(Alive=True), 
   'template_name': 'animal_list.html', 
   'template_object_name': 'animal'}, name='todo-no-cage'), url('^no_rack/$', limited_object_list, {'queryset': Animal.objects.filter(Rack__iexact='').filter(Alive=True), 
   'template_name': 'animal_list.html', 
   'template_object_name': 'animal'}, name='todo-no-rack'))