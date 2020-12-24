# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maintenance_in_progress/views.py
# Compiled at: 2014-11-11 03:11:26
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.defaults import server_error as base_server_error
from django.views.decorators.csrf import requires_csrf_token
from maintenance_in_progress.models import Preferences

def server_error(request, template_name='maintenance_in_progress/500.html'):
    """If maintenance is in progress render a friendly page"""
    p = Preferences.objects.get()
    if p.in_progress or p.file_marker and os.path.exists(p.file_marker):
        response = render_to_response(template_name, {}, context_instance=RequestContext(request))
        response['Expires'] = -1
        return response
    return base_server_error(request)