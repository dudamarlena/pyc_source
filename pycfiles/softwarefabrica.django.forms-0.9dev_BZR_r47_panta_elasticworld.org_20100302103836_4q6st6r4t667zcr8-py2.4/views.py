# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/forms/views.py
# Compiled at: 2010-02-24 10:30:59
from django.http import HttpRequest, HttpResponse
from django.db.models import get_model
from django.utils.encoding import force_unicode
from django.conf import settings
from softwarefabrica.django.utils.viewshelpers import render_to_response, json_response
import logging

def ajax_cascade_select(request):
    """
    AJAX - cascaded select support

    View that handles AJAX calls performed by SelectCascadeField and
    SelectCascadePopupField (and the associated widgets).

    Associated to the named url 'forms-ajax-cascade-select'.
    """
    assert isinstance(request, HttpRequest)
    master_app = request.REQUEST.get('master_app', request.REQUEST.get('app', ''))
    master_model_name = request.REQUEST['master_model']
    master_pk = request.REQUEST['master_id']
    slave_app = request.REQUEST.get('slave_app', master_app)
    slave_model_name = request.REQUEST['slave_model']
    slave_pivot_field = str('%s' % request.REQUEST.get('slave_pivot', 'master'))
    master_model = get_model(master_app, master_model_name)
    slave_model = get_model(slave_app, slave_model_name)
    slave_objects = slave_model.objects.filter(**{slave_pivot_field: master_pk})
    data = [ dict(pk=obj.pk, text=force_unicode(obj)) for obj in slave_objects ]
    return json_response(request, data)