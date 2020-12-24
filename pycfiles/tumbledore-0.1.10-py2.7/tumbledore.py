# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-intel/egg/tumbledore/templatetags/tumbledore.py
# Compiled at: 2013-01-29 13:42:58
from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.template.base import FilterExpression
from django.template.defaulttags import ForNode
models = __import__('tumbledore', None, None, [], 2).models
register = template.Library()
DEFAULT_NUMBER_OF_POSTS = 5

@register.tag(name='tumblevar')
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'tumblevar' node requires a variable name.")

    nodelist = parser.parse(('endtumblevar', ))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):

    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = mark_safe(self.nodelist.render(context))
        context[self.varname] = output
        return ''


@register.tag(name='tumbleposts')
def do_tumbleposts(parser, token):
    """
    Iterates given block over tumblelog posts.
    {% tumbleposts as post tumblelog_id=1 **kwargs %}
    {{ post.title }}
    {% endtumbleposts %}
    """
    bits = token.contents.split()
    bits.reverse()
    bits = [ bit.strip(',') for bit in bits ]
    tag_name = bits.pop()
    as_name = bits.pop()
    var_name = bits.pop()
    order_by = None
    kwargs_list = [ bit for bit in bits if '=' in bit ]
    kwargs = {}
    for kwarg in kwargs_list:
        key, val = kwarg.split('=')
        try:
            val = int(val)
        except ValueError:
            pass

        if val in ('True', 'False'):
            val = bool(val)
        kwargs[key] = val

    if not var_name or '=' in var_name or not kwargs.get('tumblelog_id'):
        raise template.TemplateSyntaxError("'%s' tag requires at a minimum a post variable name and tumblelog_id." % tag_name)
    order_by = None
    limit = None
    if 'order_by' in kwargs:
        order_by = kwargs['order_by']
        del kwargs['order_by']
    if 'limit' in kwargs:
        limit = kwargs['limit']
        del kwargs['limit']
    object_list = models.TumblelogPost.objects.filter(**kwargs)
    if order_by:
        object_list = object_list.order_by(order_by)
    if limit:
        object_list = object_list[:limit]
    for obj in object_list:
        permalink = reverse('tumble_post', urlconf='tumbledore.urls', args=[obj.tumblelog.mount_on, obj.slug])
        obj.__dict__.update(permalink=permalink)
        if isinstance(obj.custom_data, dict):
            obj.__dict__.update(**obj.custom_data)

    sequence = FilterExpression('', parser)
    sequence.filters = []
    sequence.var = object_list
    nodelist_loop = parser.parse(('empty', 'endtumbleposts'))
    token = parser.next_token()
    if token.contents == 'empty':
        nodelist_empty = parser.parse(('endtumbleposts', ))
        parser.delete_first_token()
    else:
        nodelist_empty = None
    return ForNode([var_name], sequence, False, nodelist_loop, nodelist_empty)