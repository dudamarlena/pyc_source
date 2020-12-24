# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/data/urls/treatment.py
# Compiled at: 2010-06-14 19:51:42
"""Url redirections for treatment objects.

This includes gneeric create, update, delete, list and detail views.
These are restricted by login required (for detail and list) and appropriate permissions for forms."""
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required, permission_required
from mousedb.data.models import Treatment
from mousedb.data.forms import TreatmentForm

@login_required
def limited_object_list(*args, **kwargs):
    return object_list(*args, **kwargs)


@login_required
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)


@permission_required('data.add_treatment')
def create_treatment(*args, **kwargs):
    return create_object(*args, **kwargs)


@permission_required('data.change_treatment')
def change_treatment(*args, **kwargs):
    return update_object(*args, **kwargs)


@permission_required('data.delete_treatment')
def delete_treatment(*args, **kwargs):
    return delete_object(*args, **kwargs)


urlpatterns = patterns('', url('^$', limited_object_list, {'queryset': Treatment.objects.all(), 
   'template_name': 'treatment_list.html', 
   'template_object_name': 'treatment'}, name='treatment-list'), url('^new/$', create_treatment, {'form_class': TreatmentForm, 
   'template_name': 'treatment_form.html'}, name='treatment-new'), url('^(?P<object_id>\\d*)/$', limited_object_detail, {'queryset': Treatment.objects.all(), 
   'template_name': 'treatment_detail.html', 
   'template_object_name': 'treatment'}, name='treatment-detail'), url('^(?P<object_id>\\d*)/edit/$', change_treatment, {'model': Treatment, 
   'template_name': 'treatment_form.html'}, name='treatment-edit'), url('^(?P<object_id>\\d*)/delete/$', delete_treatment, {'model': Treatment, 
   'post_save_redirect': '/mousedb/treatment', 
   'template_name': 'confirm_delete.html'}, name='treatment-delete'))