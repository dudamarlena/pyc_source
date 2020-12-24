# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <demo_faktury-0.0.4>\to_xml.py
# Compiled at: 2020-03-26 17:02:32
# Size of source mod 2**32: 1660 bytes
import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='  ')


def write_to_file(data, path, date_format='%Y-%m-%d'):
    """Export extracted fields to xml

    Appends .xml to path if missing and generates xml file in specified directory, if not then in root

    Parameters
    ----------
    data : dict
        Dictionary of extracted fields
    path : str
        directory to save generated xml file
    date_format : str
        Date format used in generated file

    Notes
    ----
    Do give file name to the function parameter path.
    Only `date`, `desc`, `amount` and `currency` are exported
    """
    if path.endswith('.xml'):
        filename = path
    else:
        filename = path + '.xml'
    tag_data = ET.Element('data')
    xml_file = open(filename, 'w')
    i = 0
    for line in data:
        i += 1
        tag_item = ET.SubElement(tag_data, 'item')
        tag_date = ET.SubElement(tag_item, 'date')
        tag_desc = ET.SubElement(tag_item, 'desc')
        tag_currency = ET.SubElement(tag_item, 'currency')
        tag_amount = ET.SubElement(tag_item, 'amount')
        tag_item.set('id', str(i))
        tag_date.text = line['date'].strftime(date_format)
        tag_desc.text = line['desc']
        tag_currency.text = line['currency']
        tag_amount.text = str(line['amount'])

    xml_file.write(prettify(tag_data))
    xml_file.close()