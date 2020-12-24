# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/banner/templatetags/banner_tags.py
# Compiled at: 2018-01-09 13:54:21
from django import template
from django.http import Http404
from django.utils import six
from banner.models import Banner
from banner.styles import BANNER_STYLES_MAP
register = template.Library()

@register.tag
def render_banner(parser, token):
    tokens = token.split_contents()
    if len(tokens) < 2:
        raise template.TemplateSyntaxError("Tag usage: '{% render_banner <slug or object> %} '")
    object_or_slug = tokens[1]
    kwargs = {}
    for kv in tokens[2:]:
        k, v = kv.split('=')
        kwargs[k] = v

    return BannerNode(object_or_slug, **kwargs)


class BannerNode(template.Node):

    def __init__(self, object_or_slug, **kwargs):
        self.object_or_slug = template.Variable(object_or_slug)
        self.kwargs = kwargs

    def render(self, context):
        object_or_slug = self.object_or_slug.resolve(context)
        if isinstance(object_or_slug, six.string_types):
            try:
                obj = Banner.permitted.get(slug=object_or_slug)
            except Banner.DoesNotExist:
                raise Http404(("No Banner with slug '{}' was found").format(object_or_slug))

        else:
            obj = object_or_slug
        return BANNER_STYLES_MAP[obj.style](obj).render(context)