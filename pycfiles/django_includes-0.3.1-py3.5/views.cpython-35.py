# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/django_includes/views.py
# Compiled at: 2020-01-02 03:06:44
# Size of source mod 2**32: 2899 bytes
import hashlib
from datetime import timedelta
import jwt
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotModified
from django.utils import timezone
from django.utils.http import http_date
from django.utils.module_loading import import_string
from django.views.generic import TemplateView
from django_includes.jinja2 import get_markup

def include_view(request, token, via):
    data = jwt.decode(token, settings.SECRET_KEY)
    view = import_string(data['v'])
    if hasattr(view, 'as_view'):
        view = view.as_view()
    request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
    wrapped_response = view(request, *data['a'], **data['k'])
    if wrapped_response.status_code >= 300:
        return wrapped_response
    response = HttpResponse(get_markup(view, wrapped_response, via))
    for k, v in wrapped_response.items():
        response[k] = v

    return response


class CacheableTemplateView(TemplateView):
    template_name = 'promised_views_app/cacheable.html'
    use_etag = True
    cache_control = 'private'
    max_age = 86400
    _etag = None

    def get_etag(self):
        if not self.use_etag:
            return
        if not self._etag:
            self._etag = hashlib.sha1(repr(type(self)).encode()).hexdigest()
        return self._etag

    def dispatch(self, request, *args, **kwargs):
        etag = self.get_etag()
        if etag and etag == request.META.get('HTTP_IF_NONE_MATCH', None):
            return HttpResponseNotModified()
        response = super().dispatch(request, *args, **kwargs)
        if request.is_ajax():
            if self.max_age:
                response['Expires'] = http_date((timezone.now() + timedelta(seconds=self.max_age)).timestamp())
            if self.cache_control:
                cache_control = [
                 self.cache_control]
                if self.max_age and not self.cache_control.startswith('no-'):
                    cache_control.append('max-age={}'.format(self.max_age))
                response['Cache-Control'] = ', '.join(cache_control)
            if etag:
                response['ETag'] = etag
        return response


cacheable_view = CacheableTemplateView.as_view()