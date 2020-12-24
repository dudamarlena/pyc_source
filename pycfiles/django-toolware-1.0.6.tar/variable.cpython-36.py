# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-o463eux1/django-toolware/toolware/templatetags/variable.py
# Compiled at: 2018-06-21 10:53:48
# Size of source mod 2**32: 1048 bytes
from django import template
register = template.Library()

class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ''

        context[self.var_name] = value
        return ''


@register.tag
def setvar(parser, token):
    """ {% setvar <var_name> to <var_value> %} """
    try:
        setvar, var_name, to_, var_value = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('Invalid arguments for %r' % token.split_contents()[0])

    return SetVarNode(var_name, var_value)


@register.filter()
def string2var(string):
    """
    {% with user.full_name|truncatechars:16|string2var as truncated_name %}
        {{ truncated_name|highlight:search_kw }} # need to truncated and then highlight
    {% endwith %}
    """
    return string