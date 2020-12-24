# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/turicas/software/pyenv/versions/rows/lib/python3.6/site-packages/rows/plugins/plugin_html.py
# Compiled at: 2019-02-13 03:47:25
# Size of source mod 2**32: 5410 bytes
from __future__ import unicode_literals
import six
from lxml.etree import strip_tags
from lxml.etree import tostring as to_string
from lxml.html import document_fromstring
from rows.plugins.utils import create_table, export_data, get_filename_and_fobj, serialize
try:
    from HTMLParser import HTMLParser
except:
    from html.parser import HTMLParser

try:
    from html import escape
except:
    from cgi import escape

unescape = HTMLParser().unescape

def _get_content(element):
    return (element.text if element.text is not None else '') + ''.join(to_string(child, encoding=(six.text_type)) for child in element.getchildren())


def _get_row(row, column_tag, preserve_html, properties):
    if not preserve_html:
        data = list(map(_extract_node_text, row.xpath(column_tag)))
    else:
        data = list(map(_get_content, row.xpath(column_tag)))
    if properties:
        data.append(dict(row.attrib))
    return data


def import_from_html(filename_or_fobj, encoding='utf-8', index=0, ignore_colspan=True, preserve_html=False, properties=False, table_tag='table', row_tag='tr', column_tag='td|th', *args, **kwargs):
    """Return rows.Table from HTML file."""
    filename, fobj = get_filename_and_fobj(filename_or_fobj, mode='rb')
    html = fobj.read().decode(encoding)
    html_tree = document_fromstring(html)
    tables = html_tree.xpath('//{}'.format(table_tag))
    table = tables[index]
    strip_tags(table, 'thead')
    strip_tags(table, 'tbody')
    row_elements = table.xpath(row_tag)
    table_rows = [_get_row(row, column_tag=column_tag, preserve_html=preserve_html, properties=properties) for row in row_elements]
    if properties:
        table_rows[0][-1] = 'properties'
    if preserve_html:
        if kwargs.get('fields', None) is None:
            table_rows[0] = list(map(_extract_node_text, row_elements[0]))
    if ignore_colspan:
        max_columns = max(map(len, table_rows))
        table_rows = [row for row in table_rows if len(row) == max_columns]
    meta = {'imported_from':'html',  'filename':filename,  'encoding':encoding}
    return create_table(table_rows, *args, meta=meta, **kwargs)


def export_to_html(table, filename_or_fobj=None, encoding='utf-8', *args, **kwargs):
    """Export and return rows.Table data to HTML file."""
    serialized_table = serialize(table, *args, **kwargs)
    fields = next(serialized_table)
    result = ['<table>\n\n', '  <thead>\n', '    <tr>\n']
    header = ['      <th> {} </th>\n'.format(field) for field in fields]
    result.extend(header)
    result.extend(['    </tr>\n', '  </thead>\n', '\n', '  <tbody>\n', '\n'])
    for index, row in enumerate(serialized_table, start=1):
        css_class = 'odd' if index % 2 == 1 else 'even'
        result.append('    <tr class="{}">\n'.format(css_class))
        for value in row:
            result.extend(['      <td> ', escape(value), ' </td>\n'])

        result.append('    </tr>\n\n')

    result.append('  </tbody>\n\n</table>\n')
    html = ''.join(result).encode(encoding)
    return export_data(filename_or_fobj, html, mode='wb')


def _extract_node_text(node):
    """Extract text from a given lxml node."""
    texts = map(six.text_type.strip, map(six.text_type, map(unescape, node.xpath('.//text()'))))
    return ' '.join(text for text in texts if text)


def count_tables(filename_or_fobj, encoding='utf-8', table_tag='table'):
    """Read a file passed by arg and return your table HTML tag count."""
    filename, fobj = get_filename_and_fobj(filename_or_fobj)
    html = fobj.read().decode(encoding)
    html_tree = document_fromstring(html)
    tables = html_tree.xpath('//{}'.format(table_tag))
    return len(tables)


def tag_to_dict(html):
    """Extract tag's attributes into a `dict`."""
    element = document_fromstring(html).xpath('//html/body/child::*')[0]
    attributes = dict(element.attrib)
    attributes['text'] = element.text_content()
    return attributes


def extract_text(html):
    """Extract text from a given HTML."""
    return _extract_node_text(document_fromstring(html))


def extract_links(html):
    """Extract the href values from a given HTML (returns a list of strings)."""
    return document_fromstring(html).xpath('.//@href')