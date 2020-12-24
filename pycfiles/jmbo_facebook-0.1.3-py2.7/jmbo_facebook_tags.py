# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/smirnoff/src/jmbo-facebook/jmbo_facebook/templatetags/jmbo_facebook_tags.py
# Compiled at: 2013-05-14 09:27:46
import urllib
from django import template
from django.contrib.sites.models import get_current_site
from django.conf import settings
register = template.Library()

@register.tag
def facebook_oauth_url(parser, token):
    return FacebookOauthUrlNode()


class FacebookOauthUrlNode(template.Node):

    def render(self, context):
        site = get_current_site(context['request'])
        protocol = 'http%s' % (context['request'].is_secure() and 's' or '')
        di = dict(redirect_uri=urllib.quote('%s://%s/admin/jmbo_facebook/handler' % (protocol, site.domain)), client_id=settings.JMBO_FACEBOOK['app_id'])
        url = 'https://www.facebook.com/dialog/oauth?client_id=%(client_id)s&redirect_uri=%(redirect_uri)s&scope=manage_pages' % di
        return url