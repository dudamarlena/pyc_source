# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: templateaddons/../templateaddons/templatetags/replace.py
# Compiled at: 2016-10-21 19:34:10
# Size of source mod 2**32: 1525 bytes
import re
from django import template
from django.template.defaultfilters import stringfilter
from templateaddons.utils import decode_tag_arguments, parse_tag_argument
register = template.Library()

class ReplaceNode(template.Node):

    def __init__(self, source, search='', replacement='', use_regexp=True):
        self.nodelist = source
        self.search = search
        self.replacement = replacement
        self.use_regexp = use_regexp

    def render(self, context):
        search = parse_tag_argument(self.search, context)
        replacement = parse_tag_argument(self.replacement, context)
        use_regexp = parse_tag_argument(self.use_regexp, context)
        source = self.nodelist.render(context)
        if not search:
            output = source
        else:
            if not use_regexp:
                search = re.escape(search)
            pattern = re.compile(search, re.DOTALL | re.UNICODE)
            output = re.sub(pattern, replacement, source)
        return output


def replace_tag(parser, token):
    default_arguments = {}
    default_arguments['search'] = ''
    default_arguments['replacement'] = ''
    default_arguments['use_regexp'] = True
    arguments = decode_tag_arguments(token, default_arguments)
    source = parser.parse(('endreplace', ))
    parser.delete_first_token()
    return ReplaceNode(source, **arguments)


register.tag('replace', replace_tag)

@register.filter(name='escape_regexp')
@stringfilter
def escape_regexp(value):
    return re.escape(value)