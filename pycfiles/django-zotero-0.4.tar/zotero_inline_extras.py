# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/antonio/git/festos/django_zotero/templatetags/zotero_inline_extras.py
# Compiled at: 2015-01-04 23:11:04
from django import template as t
from django.template import loader
register = t.Library()

@register.tag
def zotero_inline_tags(parser, token):
    """
    Render an inline formset of tags.
    
    Usage:
        {% zotero_inline_tags formset[ option] %}
        option = "all" | "media" | "formset"
    """
    args = token.split_contents()
    length = len(args)
    if length == 2:
        rendered_node = RenderedAllNode(args[1])
    elif length == 3 and args[2].lower() == 'all':
        rendered_node = RenderedAllNode(args[1])
    elif length == 3 and args[2].lower() == 'media':
        rendered_node = RenderedMediaNode(args[1])
    elif length == 3 and args[2].lower() == 'formset':
        rendered_node = RenderedFormsetNode(args[1])
    else:
        raise t.TemplateSyntaxError('Incorrect arguments in %s.' % args[0])
    return rendered_node


class RenderedNode(t.Node):

    def __init__(self, formset):
        self.formset = t.Variable(formset)


class RenderedAllNode(RenderedNode):

    def render(self, context):
        formset = self.formset.resolve(context)
        template = loader.get_template('zotero/inline_tags.html')
        c = t.Context({'formset': formset, 'media': True})
        return template.render(c)


class RenderedMediaNode(RenderedNode):

    def render(self, context):
        formset = self.formset.resolve(context)
        return formset.media.render()


class RenderedFormsetNode(RenderedNode):

    def render(self, context):
        formset = self.formset.resolve(context)
        template = loader.get_template('zotero/inline_tags.html')
        c = t.Context({'formset': formset, 'media': False})
        return template.render(c)