# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/middleware.py
# Compiled at: 2017-10-23 07:42:35
from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from composer.models import Slot
from composer.views import SlotView
if 'flatpages' in settings.INSTALLED_APPS:
    from django.contrib.flatpages.views import flatpage

class ComposerFallbackMiddleware(object):
    """Combine composer slot and flatpage fallbacks.
    """

    def process_response(self, request, response):
        if response.status_code != 404:
            return response
        try:
            response = SlotView.as_view()(request)
            if isinstance(response, TemplateResponse):
                return response.render()
            return response
        except Http404:
            url = request.path_info
            if not url.endswith('/') and settings.APPEND_SLASH:
                url += '/'
                try:
                    f = get_object_or_404(Slot.permitted, url=url, slot_name='content')
                    return HttpResponsePermanentRedirect('%s/' % request.path)
                except Http404:
                    pass

        if 'flatpages' not in settings.INSTALLED_APPS:
            return response
        try:
            return flatpage(request, request.path_info)
        except Http404:
            return response
        except Exception:
            if settings.DEBUG:
                raise
            return response