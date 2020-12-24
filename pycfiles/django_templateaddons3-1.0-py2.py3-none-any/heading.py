# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: templateaddons/../templateaddons/templatetags/heading.py
# Compiled at: 2016-10-21 19:34:26
import re
from django import template
from templateaddons.utils import decode_tag_arguments, parse_tag_argument
register = template.Library()

class HeadingContextNode(template.Node):

    def __init__(self, nodelist, source_level, target_level):
        self.nodelist = nodelist
        self.source_level = source_level
        self.target_level = target_level

    def render(self, context):
        source_level = parse_tag_argument(self.source_level, context)
        target_level = parse_tag_argument(self.target_level, context)
        output = self.nodelist.render(context)
        for heading_level in range(1, 7):
            from_level = heading_level + source_level - 1
            to_level = heading_level
            open_tag = re.compile('<h%d([\\s>])' % from_level, re.IGNORECASE)
            close_tag = re.compile('</h%d([\\s>])' % from_level, re.IGNORECASE)
            output = open_tag.sub('<h%d\\1' % to_level, output)
            output = close_tag.sub('</h%d\\1' % to_level, output)

        for heading_level in reversed(range(1, 7)):
            from_level = heading_level
            to_level = heading_level + target_level - 1
            open_tag = re.compile('<h%d([\\s>])' % from_level, re.IGNORECASE)
            close_tag = re.compile('</h%d([\\s>])' % from_level, re.IGNORECASE)
            output = open_tag.sub('<h%d\\1' % to_level, output)
            output = close_tag.sub('</h%d\\1' % to_level, output)

        return output


@register.tag
def headingcontext(parser, token):
    default_arguments = {}
    default_arguments['source_level'] = 1
    default_arguments['target_level'] = 2
    arguments = decode_tag_arguments(token, default_arguments)
    nodelist = parser.parse(('endheadingcontext', ))
    parser.delete_first_token()
    return HeadingContextNode(nodelist, **arguments)