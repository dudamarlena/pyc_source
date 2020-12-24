# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/animal/urls/breeding.py
# Compiled at: 2010-08-21 21:05:32
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required, permission_required
from mousedb.animal.models import Breeding
from mousedb.animal.forms import BreedingForm

@login_required
def limited_object_list(*args, **kwargs):
    return object_list(*args, **kwargs)


@permission_required('animal.add_breeding')
def create_breeding(*args, **kwargs):
    return create_object(*args, **kwargs)


@permission_required('animal.change_breeding')
def change_breeding(*args, **kwargs):
    return update_object(*args, **kwargs)


@permission_required('animal.delete_breeding')
def delete_breeding(*args, **kwargs):
    return delete_object(*args, **kwargs)


urlpatterns = patterns('', url('^$', limited_object_list, {'queryset': Breeding.objects.filter(Active=True), 
   'template_name': 'breeding_list.html', 
   'template_object_name': 'breeding', 
   'extra_context': {'breeding_type': 'Active'}}, name='breeding-list'), url('all/$', limited_object_list, {'queryset': Breeding.objects.all(), 
   'template_name': 'breeding_list.html', 
   'template_object_name': 'breeding', 
   'extra_context': {'breeding_type': 'All'}}, name='breeding-list-all'), url('^(?P<breeding_id>\\d*)/$', 'mousedb.animal.views.breeding_detail', name='breeding-detail'), url('^(?P<breeding_id>\\d*)/pups/$', 'mousedb.animal.views.breeding_pups', name='breeding-pups'), url('^(?P<breeding_id>\\d*)/change/$', 'mousedb.animal.views.breeding_change', name='breeding-pups-change'), url('^(?P<breeding_id>\\d*)/multiple/$', 'mousedb.animal.views.multiple_breeding_pups', name='animal-multiple-pups-new'), url('^new/$', create_breeding, {'form_class': BreedingForm, 
   'template_name': 'breeding_form.html', 
   'login_required': True}, name='breeding-new'), url('^(?P<object_id>\\d*)/update/$', change_breeding, {'form_class': BreedingForm, 
   'template_name': 'breeding_form.html', 
   'login_required': True}, name='breeding-edit'), url('^(?P<object_id>\\d*)/delete/$', delete_breeding, {'model': Breeding, 
   'login_required': True, 
   'post_delete_redirect': '/mousedb/breeding/', 
   'template_name': 'confirm_delete.html'}, name='breeding-delete'), url('timed_mating/$', limited_object_list, {'queryset': Breeding.objects.filter(Timed_Mating=True), 
   'template_name': 'breeding_list.html', 
   'template_object_name': 'breeding', 
   'extra_context': {'breeding_type': 'Timed Matings'}}, name='breeding-list-timed-matings'))