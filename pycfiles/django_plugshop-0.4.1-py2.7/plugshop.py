# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plugshop/templatetags/plugshop.py
# Compiled at: 2014-08-09 03:47:51
from django import template
register = template.Library()

class HasProduct(template.Node):

    def __init__(self, parser, token):
        try:
            tag_name, product = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, '%r tag requires exactly one argument' % token.contents.split()[0]

        nodelist = parser.parse(('endplusghop_has_product', ))
        parser.delete_first_token()
        self.product = parser.compile_filter(product)
        self.nodelist = nodelist

    def render(self, context, *args, **kwargs):
        return self.nodelist.render(context)


@register.tag
def plusghop_has_product(parser, token, *args, **kwargs):
    return HasProduct(parser, token)


def plugshop_currency(value):
    if value is None:
        return ''
    else:
        v = str(value)[::-1]
        return (' ').join([ v[i:i + 3][::-1] for i in xrange(0, len(v), 3) ][::-1])


register.filter('plugshop_currency', plugshop_currency)

@register.inclusion_tag('plugshop/tags/action.html')
def plugshop_action(product, action, quantity=1):
    return {'product': product, 
       'action': action, 
       'quantity': quantity}