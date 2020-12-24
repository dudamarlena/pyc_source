# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/reports/decorators.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from djblets.util.decorators import simple_decorator
from rbpowerpack.utils.extension import get_powerpack_extension

@simple_decorator
def check_reporting_enabled(view_func):
    """Check whether reports are enabled for the given local site."""

    def _check(request, local_site=None, *args, **kwargs):
        extension = get_powerpack_extension()
        local_site_name = None
        if local_site:
            local_site_name = local_site.name
        if not extension.policy.is_reporting_enabled(request.user, local_site_name):
            response = render_to_response(b'permission_denied.html', RequestContext(request))
            response.status_code = 403
            return response
        else:
            return view_func(request, local_site=local_site, extension=extension, *args, **kwargs)

    return _check