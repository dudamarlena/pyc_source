# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-contenttype-tag/generic_ct_tag/templatetags/generic_ct.py
# Compiled at: 2013-07-24 13:44:28
import re
from django import template
from django.contrib.contenttypes.models import ContentType
register = template.Library()

class ContentTypeNode(template.Node):

    def __init__(self, instance, var_name):
        self.object = template.Variable(instance)
        self.var_name = var_name

    def render(self, context):
        instance = self.object.resolve(context)
        ct = ContentType.objects.get_for_model(instance)
        if self.var_name:
            context[self.var_name] = ct
        else:
            return '%s.%s' % (ct.app_label, ct.model)


@register.tag
def content_type(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires exactly one argument' % token.contents.split()[0]

    m = re.search('(.*?) as (\\w+)', arg)
    if m:
        instance, var_name = m.groups()
    else:
        instance, var_name = arg, None
    return ContentTypeNode(instance, var_name)