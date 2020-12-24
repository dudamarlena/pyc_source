# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/antonio/git/festos/django_zotero/templatetags/zotero_tags_extras.py
# Compiled at: 2015-01-04 23:11:04
from django.template import Library, Node, TemplateSyntaxError, Variable
from django_zotero.models import Tag
register = Library()

@register.tag
def zotero_tags(parser, token):
    """
    Returns the code to be translated by Zotero.
    Usage:
        {% zotero_tags
            object=object
            vocabulary=vocabulary
            output_method=output_method %}
    Example:
        {% zotero_tags object=document1 vocabulary="dc" output_method="meta" %}
    """
    default = {'object': '', 
       'vocabulary': 'dc', 
       'output_method': 'meta'}
    letters = [
     'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven']
    min_args = 1
    max_args = len(default)
    if min_args == 1:
        min_pl = ''
    else:
        min_pl = 's'
    if max_args == 1:
        max_pl = ''
    else:
        max_pl = 's'
    args = token.split_contents()
    length = len(args)
    if length < min_args + 1:
        raise TemplateSyntaxError('%s requires at least %s argument%s.' % (
         args[0], letters[min_args], min_pl))
    else:
        if length > max_args + 1:
            raise TemplateSyntaxError('%s requires %s or less argument%s.' % (
             args[0], letters[max_args], max_pl))
        for arg in args[1:length]:
            i = arg.find('=')
            if i == -1:
                raise TemplateSyntaxError('%s syntax error: %s.' % (args[0], arg))
            else:
                key = arg[:i]
                val = arg[i + 1:]
                if key not in default.keys():
                    raise TemplateSyntaxError('%s invalid argument: %s.' % (
                     args[0], key))
                else:
                    default[key] = val

    return ZoteroTagsNode(default)


class ZoteroTagsNode(Node):

    def __init__(self, dictionary):
        self.obj = Variable(dictionary['object'])
        self.voc = Variable(dictionary['vocabulary'])
        self.out = Variable(dictionary['output_method'])

    def render(self, context):
        out = self.out.resolve(context)
        if out == 'meta':
            obj = self.obj.resolve(context)
            voc = self.voc.resolve(context)
            result = render_meta(obj, voc)
        return result


def render_meta(obj, vocabulary):
    result = '<link rel="schema.dc" href="http://purl.org/dc/elements/1.1/">'
    tags = Tag.get_tags(obj)
    if tags:
        value = tags[0].item_type.type_name
        meta_tag = '<meta property="DC.type" content="%s"/>' % value
        result = '%s\n%s' % (result, meta_tag)
        for tag in tags:
            field = tag.field
            name = field.namespaces.get(vocabulary, field.field_name)
            value = tag.value
            if name == 'identifier':
                value = '%s %s' % (field.field_name.lower(), value)
            meta_tag = '<meta property="DC.%s" content="%s"/>' % (name, value)
            result = '%s\n%s' % (result, meta_tag)

    return result