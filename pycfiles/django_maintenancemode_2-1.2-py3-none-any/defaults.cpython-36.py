# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/btaylor/work/python-projects/django-maintenancemode-2/maintenancemode/views/defaults.py
# Compiled at: 2019-12-22 19:23:11
# Size of source mod 2**32: 1171 bytes
import json
from django.template import loader, RequestContext
from django import VERSION as DJANGO_VERSION
from maintenancemode.http import HttpResponseTemporaryUnavailable
from maintenancemode.utils.settings import MAINTENANCE_503_TEMPLATE

def temporary_unavailable(request, template_name=MAINTENANCE_503_TEMPLATE):
    """
    Default 503 handler
    """
    if request.META.get('CONTENT_TYPE') == 'application/json':
        content = json.dumps({'code':503, 
         'error':'temporarily_unavailable', 
         'reason':'maintenance', 
         'error_description':'Sorry, the service is temporarily down for maintenance'})
        content_type = 'application/json'
    else:
        args = [
         template_name, {'request_path': request.path}]
        if DJANGO_VERSION < (1, 10, 0):
            args.append(RequestContext(request))
        content = (loader.render_to_string)(*args)
        content_type = 'text/html'
    return HttpResponseTemporaryUnavailable(content, content_type=content_type)