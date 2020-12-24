# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/plugins/base/group_api_urls.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import logging, re
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
from django.conf.urls import patterns, include, url
from sentry.plugins import plugins
logger = logging.getLogger('sentry.plugins')

def ensure_url(u):
    if isinstance(u, (tuple, list)):
        return url(*u)
    if not isinstance(u, (RegexURLResolver, RegexURLPattern)):
        raise TypeError('url must be RegexURLResolver or RegexURLPattern, not %r: %r' % (type(u).__name__, u))
    return u


def load_plugin_urls(plugins):
    urlpatterns = patterns('')
    for plugin in plugins:
        try:
            urls = plugin.get_group_urls()
            if not urls:
                continue
            urls = [ ensure_url(u) for u in urls ]
        except Exception:
            logger.exception('routes.failed', extra={'plugin': type(plugin).__name__})
        else:
            urlpatterns.append(url('^%s/' % re.escape(plugin.slug), include(urls)))

    return urlpatterns


urlpatterns = load_plugin_urls(plugins.all())