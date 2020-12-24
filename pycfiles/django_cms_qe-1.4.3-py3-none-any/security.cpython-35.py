# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/views/security.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 656 bytes
import json, logging
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
__all__ = ('csp_report', )

@csrf_exempt
@require_POST
def csp_report(request: HttpRequest) -> HttpResponse:
    """
    View handling reports by CSP headers. When there is problem by CSP,
    then browser fire request to this view with JSON data describing
    problem. It's simply just logged as warning for later analyzing.
    """
    data = request.read()
    data = json.loads(str(data, 'utf8', 'replace'))
    logging.warning(data)
    return HttpResponse('OK')