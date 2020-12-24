# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/animal/urls/strain.py
# Compiled at: 2010-06-20 19:21:27
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import permission_required
from django.views.generic.create_update import create_object, update_object, delete_object
from mousedb.animal.models import Strain

@permission_required('animal.add_strain')
def create_strain(*args, **kwargs):
    return create_object(*args, **kwargs)


@permission_required('animal.change_strain')
def change_strain(*args, **kwargs):
    return update_object(*args, **kwargs)


@permission_required('animal.delete_strain')
def delete_strain(*args, **kwargs):
    return delete_object(*args, **kwargs)


urlpatterns = patterns('', url('^$', 'mousedb.animal.views.strain_list', name='strain-list'), url('^new/$', create_strain, {'model': Strain, 
   'template_name': 'strain_form.html', 
   'login_required': True, 
   'post_save_redirect': '/mousedb/strain/'}, name='strain-new'), url('^(?P<object_id>\\d*)/update/$', change_strain, {'model': Strain, 
   'template_name': 'strain_form.html', 
   'login_required': True, 
   'post_save_redirect': '/mousedb/strain/'}, name='strain-edit'), url('^(?P<object_id>\\d*)/delete/$', delete_strain, {'model': Strain, 
   'login_required': True, 
   'post_delete_redirect': '/mousedb/strain/', 
   'template_name': 'confirm_delete.html'}, name='strain-delete'), url('^(?P<strain>.*)/$', 'mousedb.animal.views.strain_detail', name='strain-detail'), url('^(?P<strain>.*)/all$', 'mousedb.animal.views.strain_detail_all', name='strain-detail-all'))