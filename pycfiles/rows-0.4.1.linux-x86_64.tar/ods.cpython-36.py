# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/turicas/software/pyenv/versions/rows/lib/python3.6/site-packages/rows/plugins/ods.py
# Compiled at: 2019-02-13 03:47:25
# Size of source mod 2**32: 3920 bytes
from __future__ import unicode_literals
import zipfile
from decimal import Decimal
from lxml.etree import fromstring as xml_from_string
from lxml.etree import tostring as xml_to_string
from rows.plugins.utils import create_table, get_filename_and_fobj

def xpath(element, xpath, namespaces):
    return xml_from_string(xml_to_string(element)).xpath(xpath, namespaces=namespaces)


def attrib(cell, namespace, name):
    return cell.attrib['{{{}}}{}'.format(namespace, name)]


def complete_with_None(lists, size):
    for element in lists:
        element.extend([None] * (size - len(element)))
        yield element


def import_from_ods(filename_or_fobj, index=0, *args, **kwargs):
    filename, _ = get_filename_and_fobj(filename_or_fobj)
    ods_file = zipfile.ZipFile(filename)
    content_fobj = ods_file.open('content.xml')
    xml = content_fobj.read()
    content_fobj.close()
    document = xml_from_string(xml)
    namespaces = document.nsmap
    spreadsheet = document.xpath('//office:spreadsheet', namespaces=namespaces)[0]
    tables = xpath(spreadsheet, '//table:table', namespaces)
    table = tables[index]
    table_rows_obj = xpath(table, '//table:table-row', namespaces)
    table_rows = []
    for row_obj in table_rows_obj:
        row = []
        for cell in xpath(row_obj, '//table:table-cell', namespaces):
            children = cell.getchildren()
            if not children:
                pass
            else:
                value_type = attrib(cell, namespaces['office'], 'value-type')
                if value_type == 'date':
                    cell_value = attrib(cell, namespaces['office'], 'date-value')
                else:
                    if value_type == 'float':
                        cell_value = attrib(cell, namespaces['office'], 'value')
                    else:
                        if value_type == 'percentage':
                            cell_value = attrib(cell, namespaces['office'], 'value')
                            cell_value = Decimal(cell_value)
                            cell_value = '{:%}'.format(cell_value)
                        elif value_type == 'string':
                            try:
                                cell_value = attrib(cell, namespaces['office'], 'string-value')
                            except KeyError:
                                cell_value = children[0].text

                        else:
                            cell_value = children[0].text
                try:
                    repeat = attrib(cell, namespaces['table'], 'number-columns-repeated')
                except KeyError:
                    row.append(cell_value)
                else:
                    for _ in range(int(repeat)):
                        row.append(cell_value)

        if row:
            table_rows.append(row)

    max_length = max(len(row) for row in table_rows)
    full_rows = complete_with_None(table_rows, max_length)
    meta = {'imported_from':'ods',  'filename':filename}
    return create_table(full_rows, *args, meta=meta, **kwargs)