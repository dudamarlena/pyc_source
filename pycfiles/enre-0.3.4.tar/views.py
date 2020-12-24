# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gratromv/Projects/enresoft/enresoft/enre/views/views.py
# Compiled at: 2012-07-10 07:23:23
import datetime
from django.views.generic import TemplateView

class NoCacheMixin(object):
    no_cache = False

    def set_no_cache(self, response):
        if self.no_cache:
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = datetime.datetime.strftime(datetime.datetime.utcnow() - datetime.timedelta(seconds=1), '%a, %d %b %Y %H:%M:%S GMT')
        return response


class ScriptView(NoCacheMixin, TemplateView):
    mime_type = 'text/javascript'

    def render_to_response(self, context, **response_kwargs):
        if not response_kwargs.has_key('mimetype'):
            response_kwargs['mimetype'] = self.mime_type
        return super(ScriptView, self).render_to_response(context, **response_kwargs)

    def get(self, request, *args, **kwargs):
        return self.set_no_cache(super(ScriptView, self).get(request, *args, **kwargs))


class AjaxView(ScriptView):
    pass