# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/jmbo-and-friends/jmbo-analytics/jmbo_analytics/templatetags/jmbo_analytics_tags.py
# Compiled at: 2016-08-25 04:11:26
import urllib, urlparse
from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
from jmbo_analytics import CAMPAIGN_TRACKING_PARAMS
register = template.Library()

@register.tag
def google_analytics(parser, token):
    """Parser method that build a GoogleAnalyticsNode for rendering."""
    bits = token.split_contents()
    debug = 'False'
    if len(bits) > 1:
        debug = bits[1]
    if len(debug) > 0:
        debug = debug[0].lower() == 't'
    return GoogleAnalyticsNode(debug)


class GoogleAnalyticsNode(template.Node):
    """Tag node for building the link to the internal google analytics
    image."""

    def __init__(self, debug):
        self.debug = debug

    def render(self, context):
        try:
            assert settings.JMBO_ANALYTICS['google_analytics_id']
        except:
            return ''

        request = context.get('request', None)
        if request is None:
            raise RuntimeError('Request context required')
        params = {}
        for param in CAMPAIGN_TRACKING_PARAMS:
            value = request.GET.get(param, None)
            if value:
                params[param] = value

        referer = request.META.get('HTTP_REFERER', None)
        if referer:
            params['r'] = referer
        path = request.path
        parsed_url = urlparse.urlparse(path)
        query = urlparse.parse_qs(parsed_url.query)
        for param in params:
            if query.has_key(param):
                del query[param]

        query = urllib.urlencode(query)
        new_url = parsed_url._replace(query=query)
        params['p'] = new_url.geturl()
        if self.debug:
            params['utmdebug'] = 1
        url = reverse('google-analytics')
        if len(params) > 0:
            url += '?' + urllib.urlencode(params)
        return url