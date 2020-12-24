# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/views/errors.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 2971 bytes
import logging
from typing import Callable
from cms.views import details
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.http.response import HttpResponseBase
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from django.utils.translation import ugettext as _
__all__ = ('handler403', 'handler404', 'handler500', 'handler503', 'get_error_handler')

def get_error_handler--- This code section failed: ---

 L.  32         0  LOAD_GLOBAL              requires_csrf_token

 L.  33         3  LOAD_GLOBAL              HttpRequest
                6  LOAD_GLOBAL              HttpResponseBase
                9  LOAD_CONST               ('request', 'return')
               12  LOAD_CLOSURE             'code'
               15  BUILD_TUPLE_1         1 
               18  LOAD_CODE                <code_object error_handler>
               21  LOAD_STR                 'get_error_handler.<locals>.error_handler'
               24  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               30  CALL_FUNCTION_1       1  '1 positional, 0 named'
               33  STORE_FAST               'error_handler'

 L.  52        36  LOAD_FAST                'error_handler'
               39  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CODE' instruction at offset 18


handler403 = get_error_handler(403)
handler404 = get_error_handler(404)
handler503 = get_error_handler(503)

@requires_csrf_token
def handler500(request: HttpRequest) -> HttpResponseBase:
    """
    When application fail on internal error, Django CMS has problem
    to render any page. They don't have any API for rendering any page
    so it's imposible to get it right. Solution could be just redirect
    to page with given slug but it could also hang in infinite loop of
    redirection if there would be problem on page with slug error500.

    That's why we simply just use different template which cannot be
    changed in admin by user. To override default template, just create
    your own ``cms_qe/internal_error.html`` or change ``handler500``
    to your own view.
    """
    try:
        return render(request, 'cms_qe/internal_error.html')
    except Exception:
        logging.exception('Exception while rendering page 500')
        return HttpResponse('<h1>{}</h1><p>{}</p>'.format(_('Internal error'), _('Something went very wrong. Please try again later.')))