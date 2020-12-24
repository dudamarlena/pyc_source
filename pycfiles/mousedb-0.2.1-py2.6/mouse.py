# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/animal/urls/mouse.py
# Compiled at: 2010-08-21 21:05:32
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required, permission_required
from mousedb.animal.forms import AnimalForm

@login_required
def limited_object_list(*args, **kwargs):
    return object_list(*args, **kwargs)


@permission_required('animal.add_animal')
def create_animal(*args, **kwargs):
    return create_object(*args, **kwargs)


@permission_required('animal.change_animal')
def change_animal(*args, **kwargs):
    return update_object(*args, **kwargs)


@permission_required('animal.delete_animal')
def delete_animal(*args, **kwargs):
    return delete_object(*args, **kwargs)


from mousedb.animal.models import Animal
urlpatterns = patterns('', url('^$', limited_object_list, {'queryset': Animal.objects.filter(Alive=True), 
   'template_name': 'animal_list.html', 
   'template_object_name': 'animal', 
   'extra_context': {'list_type': 'Alive'}}, name='animal-list'), url('all/?$', limited_object_list, {'queryset': Animal.objects.all(), 
   'template_name': 'animal_list.html', 
   'template_object_name': 'animal'}, name='animal-list-all'), url('^(?P<id>\\d*)/$', 'mousedb.animal.views.animal_detail', name='animal-detail'), url('^new/$', create_animal, {'form_class': AnimalForm, 
   'template_name': 'animal_form.html', 
   'login_required': True, 
   'post_save_redirect': '/mousedb/mouse/'}, name='animal-new'), url('^(?P<object_id>\\d*)/update/$', change_animal, {'form_class': AnimalForm, 
   'template_name': 'animal_form.html', 
   'login_required': True, 
   'post_save_redirect': '/mousedb/mouse/'}, name='animal-update'), url('^(?P<object_id>\\d*)/delete/$', delete_animal, {'model': Animal, 
   'login_required': True, 
   'post_delete_redirect': '/mousedb/mouse/', 
   'template_name': 'confirm_delete.html'}, name='animal-delete'), url('^new/multiple/$', 'mousedb.animal.views.multiple_pups', name='animal-multiple-new'))