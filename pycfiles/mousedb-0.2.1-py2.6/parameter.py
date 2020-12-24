# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/data/urls/parameter.py
# Compiled at: 2010-06-14 19:51:42
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required
from mousedb.data.models import Pharmaceutical, Diet

@login_required
def limited_object_list(*args, **kwargs):
    return object_list(*args, **kwargs)


@login_required
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)


urlpatterns = patterns('', (
 '^pharmaceuticals?/(?P<object_id>\\d*)', limited_object_detail,
 {'queryset': Pharmaceutical.objects.all(), 
    'template_name': 'pharmaceutical_detail.html', 
    'template_object_name': 'pharmaceutical'}), (
 '^diets?/(?P<object_id>\\d*)', limited_object_detail,
 {'queryset': Diet.objects.all(), 
    'template_name': 'diet_detail.html', 
    'template_object_name': 'diet'}))