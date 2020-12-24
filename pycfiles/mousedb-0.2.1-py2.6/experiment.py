# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/data/urls/experiment.py
# Compiled at: 2010-08-21 21:05:32
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required, permission_required
from mousedb.data.forms import ExperimentForm
from mousedb.data.models import Measurement, Experiment

@login_required
def limited_object_list(*args, **kwargs):
    return object_list(*args, **kwargs)


@login_required
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)


@permission_required('data.add_experiment')
def create_experiment(*args, **kwargs):
    return create_object(*args, **kwargs)


@permission_required('data.change_experiment')
def change_experiment(*args, **kwargs):
    return update_object(*args, **kwargs)


@permission_required('data.delete_experiment')
def delete_experiment(*args, **kwargs):
    return delete_object(*args, **kwargs)


urlpatterns = patterns('', url('^$', 'mousedb.data.views.experiment_list', name='experiment-list'), url('^(?P<object_id>\\d*)/$', limited_object_detail, {'queryset': Experiment.objects.all(), 
   'template_name': 'experiment_detail.html', 
   'template_object_name': 'experiment'}, name='experiment-detail'), url('^(?P<experiment_id>\\d*)/csv', 'mousedb.data.views.experiment_details_csv', name='experiment-detail-csv'), url('^(?P<experiment_id>\\d*)/data_entry/$', 'mousedb.data.views.add_measurement', name='data-entry'), url('^new/$', create_experiment, {'form_class': ExperimentForm, 
   'template_name': 'experiment_form.html', 
   'login_required': True, 
   'post_save_redirect': '/mousedb/experiment/'}, name='experiment-new'), url('^data/all$', limited_object_list, {'queryset': Measurement.objects.all(), 
   'template_name': 'data.html', 
   'template_object_name': 'data'}, name='measurement_list'))