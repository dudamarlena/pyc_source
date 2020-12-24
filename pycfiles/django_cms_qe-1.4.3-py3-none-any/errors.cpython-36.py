# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
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

def get_error_handler(code: int) -> Callable[([HttpRequest], HttpResponseBase)]:
    """
    Decorator creating error handler for specific HTTP status code.

    When CMS page with slug ``errorCODE`` exists, then is shown that
    page, otherwise generic one. Page is not cached because of that.

    Possible slugs:

     * error403 (forbidden)
     * error404 (not found)
     * error503 (service unavailable)
    """

    @requires_csrf_token
    def error_handler(request, *args, **kwds):
        slug = 'error{}'.format(code)
        if hasattr(request, '_current_page_cache'):
            delattr(request, '_current_page_cache')
        try:
            response = details(request, slug)
        except Http404:
            response = render(request, 'cms_qe/error.html', context={'slug': slug})

        if response:
            if not settings.DEBUG:
                response.status_code = code
        return response

    return error_handler


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