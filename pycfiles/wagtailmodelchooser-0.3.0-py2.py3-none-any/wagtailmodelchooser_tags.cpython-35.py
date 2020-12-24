# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/leo/Devel/Naeka/wagtailmodelchooser/wagtailmodelchooser/templatetags/wagtailmodelchooser_tags.py
# Compiled at: 2018-11-19 13:04:53
# Size of source mod 2**32: 1114 bytes
from django import template
register = template.Library()

@register.filter
def getattr(obj, attr_name):
    try:
        assert obj is not None
        return obj.__getattribute__(attr_name)
    except AttributeError:
        return obj.__dict__.get(attr_name, '')
    except:
        return ''


@register.tag(name='captureas')
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires a variable name.")

    nodelist = parser.parse(('endcaptureas', ))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):

    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''