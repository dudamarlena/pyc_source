# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/glyphviewer/templatetags/glyphtable.py
# Compiled at: 2018-03-17 21:22:04
from glyphviewer.glyphviewer import glyphCatcher, glyphArray, fontHeader, DODGY
from django import template
from django.utils.safestring import mark_safe
DEFAULT_GLYPHTABLE_SIZE = 16
TABSUM = '<table style="table-layout: fixed; width:100%;" class="glyphtable table-bordered table-styled">\n'
TABCAP = '<caption class="glyphcaption"><strong>%s</strong></caption>\n<tbody class="glyphtbody">\n'
CELLMAKER = '<td class = "glyphtd"><p class = "glyphchar text-center">&#%s;<br />\n<p class = "glyphnum text-center"><strong>U+%04X</strong></p></td>'
REMAINDER = '<td class = "glyphempty"><p class="glyphchar text-center">&nbsp;</p><p class="glyphnum text-center">&nbsp;</p></td>'
register = template.Library()

@register.filter(name='glyphtable')
def glyphtable(value, arg=DEFAULT_GLYPHTABLE_SIZE):
    """ Takes an argument (value) that is assumed to be of type glyphArray.
    The function returns HTML that represents all the glyphs as a table. The
    arg argument indicates the number of columns for the table.

    Note: many of the generated entries are given HTML classes - all the
    better for CSS styling.

    """
    try:
        if value.blockName == DODGY:
            if len(value.codePoints) == 0:
                return ''
            output = '<p><em>Note: the following numbers listed are the code '
            output += 'point values of characters in the font that would '
            output += 'normally not be printed, such as control characters. '
            output += 'For that reason, they are represented separately.</em></p>\n'
            output += '<ul>\n'
            for i in value.codePoints:
                output += '<li>U+%04X</li>\n' % i

            output += '</ul>\n'
            return mark_safe(output)
        else:
            blocksize = len(value.codePoints)
            numfullrows = blocksize / arg
            remainder = blocksize % arg
            output = TABSUM + TABCAP % value.blockName
            for i in range(numfullrows):
                output += '<tr class = "glyphtr">'
                for j in range(arg):
                    ournumber = value.codePoints[(j + i * arg)]
                    output += CELLMAKER % (str(ournumber), ournumber)

                output += '</tr>\n'

            if remainder == 0:
                output += '</tbody>\n</table>\n'
                return mark_safe(output)
            output += '<tr class = "glyphtr">'
            for j in range(remainder):
                ournumber = value.codePoints[(j + numfullrows * arg)]
                output += CELLMAKER % (str(ournumber), ournumber)

            for j in range(arg - remainder):
                output += REMAINDER

            output += '</tr>\n'
            output += '</tbody>\n</table>\n'
            return mark_safe(output)

    except:
        return ''


glyphtable.is_safe = False

@register.inclusion_tag('glyphviewer/showheader.html')
def showheader(value):
    return {'value': value}