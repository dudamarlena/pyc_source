# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/metaimage/templatetags/metaimage_tags.py
# Compiled at: 2011-02-15 19:26:42
import re
from django import template
register = template.Library()

@register.tag(name='print_exif')
def do_print_exif(parser, token):
    try:
        (tag_name, exif) = token.contents.split()
    except ValueError:
        msg = '%r tag requires a single argument' % token.contents[0]
        raise template.TemplateSyntaxError(msg)

    exif = parser.compile_filter(exif)
    return PrintExifNode(exif)


class PrintExifNode(template.Node):

    def __init__(self, exif):
        self.exif = exif

    def render(self, context):
        try:
            exif = unicode(self.exif.resolve(context, True))
        except template.VariableDoesNotExist:
            exif = ''

        EXPR = "'(?P<key>[^:]*)'\\:(?P<value>[^,]*),"
        expr = re.compile(EXPR)
        msg = '<table>'
        for i in expr.findall(exif):
            msg += '<tr><td>%s</td><td>%s</td></tr>' % (i[0], i[1])

        msg += '</table>'
        return '<div id="exif">%s</div>' % msg