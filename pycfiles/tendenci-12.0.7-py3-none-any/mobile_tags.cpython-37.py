# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/mobile/templatetags/mobile_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 1117 bytes
from django import template
from django.urls import reverse
from django.template import TemplateSyntaxError, Variable
import django.utils.translation as _
register = template.Library()

class MobileLinkNode(template.Node):

    def __init__(self, redirect_url, link_name):
        self.redirect_url = redirect_url
        self.link_name = link_name

    def render(self, context):
        try:
            redirect_url = Variable(self.redirect_url)
            redirect_url = redirect_url.resolve(context)
        except:
            redirect_url = self.redirect_url

        return "<a href='%s?next=%s'>%s</a>" % (
         reverse('toggle_mobile_mode'),
         redirect_url,
         self.link_name)


@register.tag(name='toggle_mobile_link')
def toggle_mobile_link(parser, token):
    """
    {% toggle_mobile_link request.get_full_path "See mobile" %}
    """
    bits = token.split_contents()
    if len(bits) > 3:
        message = "'%s' tag requires exactly 2 arguments" % bits[0]
        raise TemplateSyntaxError(_(message))
    return MobileLinkNode(bits[1], bits[2][1:-1])