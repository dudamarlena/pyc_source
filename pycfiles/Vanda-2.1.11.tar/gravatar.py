# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/vanda/vanda/core/templatetags/gravatar.py
# Compiled at: 2013-01-07 03:52:15
import urllib, hashlib
from django import template
from django.conf import settings
register = template.Library()

class GravatarUrlNode(template.Node):

    def __init__(self, email, size=None, host=None):
        self.email = template.Variable(email)
        self.size = size
        self.host = host

    def render(self, context):
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        size = 40
        if self.size:
            size = self.size
        if self.host:
            host = self.host
        else:
            host = context['request'].META['HTTP_HOST']
        default = 'http://%s%simages/defaultavatar.png' % (host, settings.MEDIA_URL)
        gravatar_url = 'http://www.gravatar.com/avatar/%s?' % hashlib.md5(email.lower()).hexdigest()
        gravatar_url += urllib.urlencode({'d': default, 's': str(size)})
        return gravatar_url


@register.tag
def gravatar_url(parser, token):
    try:
        tag_name, email, size, host = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires two argument' % token.contents.split()[0]

    return GravatarUrlNode(email, int(size), host)