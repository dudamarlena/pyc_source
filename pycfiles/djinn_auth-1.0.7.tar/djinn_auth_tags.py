# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_auth/djinn_auth/templatetags/djinn_auth_tags.py
# Compiled at: 2014-12-08 06:02:47
from django.template import Library
from django.template.base import NodeList
from django.template.defaulttags import IfNode, TemplateLiteral
register = Library()

class HasPermissionNode(IfNode):

    def __init__(self, ctx, user, perm, nodelist_true, nodelist_false=None):
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.ctx = ctx
        self.usr = user
        self.perm = perm

    def render(self, context):
        ctx = self.ctx.eval(context)
        usr = self.usr.eval(context)
        if hasattr(self.perm, 'eval'):
            perm = self.perm.eval(context)
        else:
            perm = self.perm
        if ctx and perm in ('delete', 'change', 'add', 'view'):
            perm = '%s.%s_%s' % (ctx._meta.app_label, perm,
             ctx._meta.object_name.lower())
        if usr.has_perm(perm, obj=ctx):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


def if_has_perm(parser, token):
    """ Usage: if_has_perm <context> <user object> '<permission codename>'"""
    bits = token.split_contents()[1:]
    ctx = TemplateLiteral(parser.compile_filter(bits[0]), bits[0])
    user = TemplateLiteral(parser.compile_filter(bits[1]), bits[1])
    perm = TemplateLiteral(parser.compile_filter(bits[2]), bits[2])
    nodelist_true = parser.parse(('else', 'endif_has_perm'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_has_perm', ))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return HasPermissionNode(ctx, user, perm, nodelist_true, nodelist_false)


register.tag('if_has_perm', if_has_perm)