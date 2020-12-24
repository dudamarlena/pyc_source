# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/templatetags/difftags.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import re
from django import template
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from reviewboard.diffviewer.chunk_generator import DiffChunkGenerator
register = template.Library()

@register.filter
def highlightregion(value, regions):
    """Highlights the specified regions of text.

    This is used to insert ``<span class="hl">...</span>`` tags in the
    text as specified by the ``regions`` variable.
    """
    if not regions:
        return value
    html = []
    in_hl = False
    i = j = r = 0
    region_start, region_end = regions[r]
    while i < len(value):
        c = value[i]
        if c == b'<':
            if in_hl:
                html.append(b'</span>')
                in_hl = False
            k = value.find(b'>', i)
            assert k != -1
            html.append(value[i:k + 1])
            i = k
        else:
            if not in_hl and region_start <= j < region_end:
                html.append(b'<span class="hl">')
                in_hl = True
            if c == b'&':
                k = value.find(b';', i)
                assert k != -1
                html.append(value[i:k + 1])
                i = k
                j += 1
            else:
                j += 1
                html.append(c)
        if j == region_end:
            if in_hl:
                html.append(b'</span>')
                in_hl = False
            r += 1
            if r == len(regions):
                break
            region_start, region_end = regions[r]
        i += 1

    if i + 1 < len(value):
        html.append(value[i + 1:])
    return mark_safe((b'').join(html))


extraWhitespace = re.compile(b'(\\s+(</span>)?$| +\\t)')

@register.filter
def showextrawhitespace(value):
    """
    Marks up any extra whitespace in the specified text.

    Any trailing whitespace or tabs following one or more spaces are
    marked up by inserted ``<span class="ew">...</span>`` tags.
    """
    value = extraWhitespace.sub(b'<span class="ew">\\1</span>', value)
    return value.replace(b'\t', b'<span class="tb">\t</span>')


showextrawhitespace.is_safe = True

def _diff_expand_link(context, expandable, text, tooltip, expand_pos, image_class):
    """Utility function to render a diff expansion link.

    This is used internally by other template tags to provide a diff
    expansion link. It assumes nothing about the content and serves only
    to render the data from a template.
    """
    return render_to_string(b'diffviewer/expand_link.html', {b'tooltip': tooltip, 
       b'text': text, 
       b'chunk': context[b'chunk'], 
       b'file': context[b'file'], 
       b'expand_pos': expand_pos, 
       b'image_class': image_class, 
       b'expandable': expandable})


@register.simple_tag(takes_context=True)
def diff_expand_link(context, expanding, tooltip, expand_pos_1=None, expand_pos_2=None, text=None):
    """Renders a diff expansion link.

    This link will expand the diff entirely, or incrementally in one
    or more directions.

    'expanding' is expected to be one of 'all', 'above', or 'below'.
    """
    if expanding == b'all':
        image_class = b'rb-icon-diff-expand-all'
        expand_pos = None
    else:
        lines_of_context = context[b'lines_of_context']
        expand_pos = (lines_of_context[0] + expand_pos_1,
         lines_of_context[1] + expand_pos_2)
        image_class = b'rb-icon-diff-expand-%s' % expanding
    return _diff_expand_link(context, True, text, tooltip, expand_pos, image_class)


@register.simple_tag(takes_context=True)
def diff_chunk_header(context, header):
    """Renders a diff header as HTML.

    This diff header may be expandable, depending on whether or not the
    function/class referenced in the header is contained within the collapsed
    region.
    """
    lines_of_context = context[b'lines_of_context']
    chunk = context[b'chunk']
    line = chunk[b'lines'][0]
    if header[b'line'] >= line[1]:
        expand_offset = line[1] + chunk[b'numlines'] - header[b'line']
        expandable = True
    else:
        expand_offset = 0
        expandable = False
    return _diff_expand_link(context, expandable, b'<code>%s</code>' % escape(header[b'text']), _(b'Expand to header'), (
     lines_of_context[0],
     expand_offset + lines_of_context[1]), b'rb-icon-diff-expand-header')


@register.simple_tag
def diff_lines(index, chunk, standalone, line_fmt, anchor_fmt=b'', begin_collapse_fmt=b'', end_collapse_fmt=b'', moved_fmt=b''):
    """Renders the lines of a diff.

    This will render each line in the diff viewer. The function expects
    some basic data on what will be rendered, as well as printf-formatted
    templates for the contents.

    printf-formatted templates are used instead of standard Django templates
    because they're much faster to render, which makes a huge difference
    when rendering thousands of lines or more.
    """
    lines = chunk[b'lines']
    num_lines = len(lines)
    chunk_index = chunk[b'index']
    change = chunk[b'change']
    is_equal = False
    is_replace = False
    is_insert = False
    is_delete = False
    if change == b'equal':
        is_equal = True
    else:
        if change == b'replace':
            is_replace = True
        elif change == b'insert':
            is_insert = True
        elif change == b'delete':
            is_delete = True
        result = []
        for i, line in enumerate(lines):
            row_classes = []
            header_1_classes = []
            header_2_classes = []
            cell_1_classes = [b'l']
            cell_2_classes = [b'r']
            row_class_attr = b''
            header_1_class_attr = b''
            header_2_class_attr = b''
            cell_1_class_attr = b''
            cell_2_class_attr = b''
            line1 = line[2]
            line2 = line[5]
            linenum1 = line[1]
            linenum2 = line[4]
            show_collapse = False
            anchor = None
            if i == 0:
                row_classes.append(b'first')
            if i == num_lines - 1:
                row_classes.append(b'last')
            if not is_equal:
                if i == 0:
                    anchor = b'%s.%s' % (index, chunk_index)
                if line[7]:
                    row_classes.append(b'whitespace-line')
                if is_replace:
                    if len(line1) < DiffChunkGenerator.STYLED_MAX_LINE_LEN:
                        line1 = highlightregion(line1, line[3])
                    if len(line2) < DiffChunkGenerator.STYLED_MAX_LINE_LEN:
                        line2 = highlightregion(line2, line[6])
            else:
                show_collapse = i == 0 and standalone
            if not is_insert and len(line1) < DiffChunkGenerator.STYLED_MAX_LINE_LEN:
                line1 = showextrawhitespace(line1)
            if not is_delete and len(line2) < DiffChunkGenerator.STYLED_MAX_LINE_LEN:
                line2 = showextrawhitespace(line2)
            moved_from = {}
            moved_to = {}
            is_moved_row = False
            is_first_moved_row = False
            if len(line) > 8 and isinstance(line[8], dict):
                moved_info = line[8]
                if b'from' in moved_info:
                    moved_from_linenum, moved_from_first = moved_info[b'from']
                    is_moved_row = True
                    header_2_classes.append(b'moved-from')
                    cell_2_classes.append(b'moved-from')
                    if moved_from_first:
                        is_first_moved_row = True
                        header_2_classes.append(b'moved-from-start')
                        cell_2_classes.append(b'moved-from-start')
                        moved_from = {b'class': b'moved-flag', 
                           b'line': mark_safe(b'moved-from-%s' % moved_from_linenum), 
                           b'target': mark_safe(b'moved-to-%s' % linenum2), 
                           b'text': _(b'Moved from line %s') % moved_from_linenum}
                if b'to' in moved_info:
                    moved_to_linenum, moved_to_first = moved_info[b'to']
                    is_moved_row = True
                    header_1_classes.append(b'moved-to')
                    cell_1_classes.append(b'moved-to')
                    if moved_to_first:
                        is_first_moved_row = True
                        header_1_classes.append(b'moved-to-start')
                        cell_1_classes.append(b'moved-to-start')
                        moved_to = {b'class': b'moved-flag', 
                           b'line': mark_safe(b'moved-to-%s' % moved_to_linenum), 
                           b'target': mark_safe(b'moved-from-%s' % linenum1), 
                           b'text': _(b'Moved to line %s') % moved_to_linenum}
            if is_moved_row:
                row_classes.append(b'moved-row')
            if is_first_moved_row:
                row_classes.append(b'moved-row-start')
            if row_classes:
                row_class_attr = b' class="%s"' % (b' ').join(row_classes)
            if cell_1_classes:
                cell_1_class_attr = b' class="%s"' % (b' ').join(cell_1_classes)
            if cell_2_classes:
                cell_2_class_attr = b' class="%s"' % (b' ').join(cell_2_classes)
            if header_1_classes:
                header_1_class_attr = b' class="%s"' % (b' ').join(header_1_classes)
            if header_2_classes:
                header_2_class_attr = b' class="%s"' % (b' ').join(header_2_classes)
            anchor_html = b''
            begin_collapse_html = b''
            end_collapse_html = b''
            moved_from_html = b''
            moved_to_html = b''
            context = {b'chunk_index': chunk_index, 
               b'row_class_attr': row_class_attr, 
               b'header_1_class_attr': header_1_class_attr, 
               b'header_2_class_attr': header_2_class_attr, 
               b'cell_1_class_attr': cell_1_class_attr, 
               b'cell_2_class_attr': cell_2_class_attr, 
               b'linenum_row': line[0], 
               b'linenum1': linenum1, 
               b'linenum2': linenum2, 
               b'line1': line1, 
               b'line2': line2, 
               b'moved_from': moved_from, 
               b'moved_to': moved_to}
            if anchor:
                anchor_html = anchor_fmt % {b'anchor': anchor}
            if show_collapse:
                begin_collapse_html = begin_collapse_fmt % context
                end_collapse_html = end_collapse_fmt % context
            if moved_from:
                moved_from_html = moved_fmt % moved_from
            if moved_to:
                moved_to_html = moved_fmt % moved_to
            context.update({b'anchor_html': anchor_html, 
               b'begin_collapse_html': begin_collapse_html, 
               b'end_collapse_html': end_collapse_html, 
               b'moved_from_html': moved_from_html, 
               b'moved_to_html': moved_to_html})
            result.append(line_fmt % context)

    return (b'').join(result)