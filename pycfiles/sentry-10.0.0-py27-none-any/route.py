# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/debug/panels/route.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.template import Context, Template
from debug_toolbar.panels import Panel
TEMPLATE = Template('\n{% load i18n %}\n<h4>{% trans "Route" %}</h4>\n<table>\n    <tr>\n        <th>Response Code</th>\n        <td>{{ response_code }}</td>\n    </tr>\n    <tr>\n        <th>View</th>\n        <td><code>{{ view_path }}</code></td>\n    </tr>\n    <tr>\n        <th>Args</th>\n        <td><code>{{ view_argspec }}</code></td>\n    </tr>\n</table>\n')

class RoutePanel(Panel):
    title = 'Route'
    template = 'sentry/debug/panels/route.html'
    has_content = True

    def _get_func_name(self, func):
        if hasattr(func, 'im_class'):
            return ('{}.{}.{}').format(func.__module__, func.im_class.__name__, func.__name__)
        return ('{}.{}').format(func.__module__, func.__name__)

    def _get_func_argspec(self, args, kwargs):
        result = []
        for arg in args:
            result.append(arg)

        for pair in kwargs.items():
            result.append('%s=%s' % tuple(pair))

        return (', ').join(result)

    def nav_subtitle(self):
        stats = self.get_stats()
        return stats['view_name']

    @property
    def content(self):
        stats = self.get_stats()
        return TEMPLATE.render(Context(stats))

    def process_view(self, request, view_func, view_args, view_kwargs):
        self._view = [
         view_func, view_args, view_kwargs]

    def process_response(self, request, response):
        stats = {}
        if hasattr(self, '_view'):
            view_func, view_args, view_kwargs = self._view
            stats['response_code'] = response.status_code
            stats['view_name'] = view_func.__name__
            stats['view_path'] = self._get_func_name(view_func)
            stats['view_argspec'] = self._get_func_argspec(view_args, view_kwargs)
        self.record_stats(stats)