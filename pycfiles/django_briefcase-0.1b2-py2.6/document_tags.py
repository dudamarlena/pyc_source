# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\briefcase\templatetags\document_tags.py
# Compiled at: 2010-10-21 13:33:32
"""
Templatetags definitions.
"""
from django.template import Library, Node, TemplateSyntaxError
from django.utils.translation import ugettext_lazy as _
from briefcase.models import DocumentType
register = Library()

def do_get_document_types(parser, token):
    """
    Retrieves a list of all distinct document types found in the database.
    """
    bits = token.split_contents()
    if len(bits) != 3:
        raise TemplateSyntaxError(_('%s requires 2 arguments') % bits[0])
    if bits[1] != 'as':
        raise TemplateSyntaxError(_("Second argument of %s must be 'as'") % bits[0])
    as_varname = bits[2]
    return DocumentTypesNode(as_varname)


class DocumentTypesNode(Node):
    """
    Inserts document type list into the template context.
    """

    def __init__(self, as_varname):
        self.as_varname = as_varname

    def render(self, context):
        document_types = DocumentType.objects.exclude(extension__exact='').order_by('extension')
        context[self.as_varname] = document_types
        return ''


register.tag('get_document_types', do_get_document_types)