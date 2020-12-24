# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/generic.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import os, posixpath
from django.conf import settings
from django.http import HttpResponseNotFound, Http404
from django.contrib.staticfiles import finders
from django.utils.six.moves.urllib.parse import unquote
from django.views import static
from django.views.generic import TemplateView as BaseTemplateView
from sentry.web.helpers import render_to_response
FOREVER_CACHE = 'max-age=315360000'
NEVER_CACHE = 'max-age=0, no-cache, no-store, must-revalidate'

def dev_favicon(request):
    document_root, path = resolve('sentry/images/favicon_dev.png')
    return static.serve(request, path, document_root=document_root)


def resolve(path):
    normalized_path = posixpath.normpath(unquote(path)).lstrip('/')
    try:
        absolute_path = finders.find(normalized_path)
    except Exception:
        absolute_path = None

    if not absolute_path:
        raise Http404("'%s' could not be found" % path)
    if path[(-1)] == '/' or os.path.isdir(absolute_path):
        raise Http404('Directory indexes are not allowed here.')
    return os.path.split(absolute_path)


def static_media(request, **kwargs):
    """
    Serve static files below a given point in the directory structure.
    """
    module = kwargs.get('module')
    path = kwargs.get('path', '')
    version = kwargs.get('version')
    if module:
        path = '%s/%s' % (module, path)
    try:
        document_root, path = resolve(path)
    except Http404:
        return HttpResponseNotFound('', content_type='text/plain')

    if 'gzip' in request.META.get('HTTP_ACCEPT_ENCODING', '') and not path.endswith('.gz') and not settings.DEBUG:
        paths = (path + '.gz', path)
    else:
        paths = (
         path,)
    for p in paths:
        try:
            response = static.serve(request, p, document_root=document_root)
            break
        except Http404:
            continue

    response['Vary'] = 'Accept-Encoding'
    if path.endswith(('.js', '.ttf', '.ttc', '.otf', '.eot', '.woff', '.woff2')):
        response['Access-Control-Allow-Origin'] = '*'
    if version is not None and not settings.DEBUG:
        response['Cache-Control'] = FOREVER_CACHE
    else:
        response['Cache-Control'] = NEVER_CACHE
    return response


class TemplateView(BaseTemplateView):

    def render_to_response(self, context, **response_kwargs):
        return render_to_response(request=self.request, template=self.get_template_names(), context=context, **response_kwargs)