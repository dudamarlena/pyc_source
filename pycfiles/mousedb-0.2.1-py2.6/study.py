# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/data/urls/study.py
# Compiled at: 2010-06-20 21:03:38
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required, permission_required
from mousedb.data.models import Study
from mousedb.data.forms import StudyForm

@login_required
def limited_object_list(*args, **kwargs):
    return object_list(*args, **kwargs)


@login_required
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)


@permission_required('data.add_study')
def create_study(*args, **kwargs):
    return create_object(*args, **kwargs)


@permission_required('data.change_study')
def change_study(*args, **kwargs):
    return update_object(*args, **kwargs)


@permission_required('data.delete_study')
def delete_study(*args, **kwargs):
    return delete_object(*args, **kwargs)


urlpatterns = patterns('', url('^$', limited_object_list, {'queryset': Study.objects.all(), 
   'template_name': 'study_list.html', 
   'template_object_name': 'study'}, name='study-list'), url('^new/$', create_study, {'form_class': StudyForm, 
   'template_name': 'study_form.html'}, name='study-new'), url('^(?P<object_id>\\d*)/$', limited_object_detail, {'queryset': Study.objects.all(), 
   'template_name': 'study_detail.html', 
   'template_object_name': 'study'}, name='study-detail'), url('^(?P<object_id>\\d*)/edit/$', change_study, {'model': Study, 
   'template_name': 'study_form.html'}, name='study-edit'), url('^(?P<object_id>\\d*)/delete/$', delete_study, {'model': Study, 
   'post_save_redirect': '/mousedb/study', 
   'template_name': 'confirm_delete.html'}, name='study-delete'), url('^(?P<study_id>\\d*)/experiment/new/$', 'mousedb.data.views.study_experiment'))