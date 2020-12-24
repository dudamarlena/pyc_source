# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vellum/templatetags/vellum_archives.py
# Compiled at: 2012-04-05 15:23:57
import re
from django import template
from vellum.models import Post
register = template.Library()

class PostArchive(template.Node):

    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        dates = Post.objects.published().dates('publish', 'month', order='DESC')
        if dates:
            context[self.var_name] = dates
        return ''


@register.tag
def get_post_archive(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError('%s tag requires arguments' % token.contents.split()[0])

    m = re.search('as (\\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError('%s tag had invalid arguments' % tag_name)
    var_name = m.groups()[0]
    return PostArchive(var_name)