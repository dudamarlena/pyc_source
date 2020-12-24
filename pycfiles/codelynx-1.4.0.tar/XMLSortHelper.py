# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Python27\Lib\site-packages\CodeLibWrapper\Src\XMLFunction\XMLSortHelper.py
# Compiled at: 2016-12-09 03:08:26
from operator import attrgetter
import lxml.etree as le

def sort_by_int_type(elem, attr_name):
    attr_obj = elem.get(attr_name)
    if attr_obj:
        try:
            return int(attr_obj)
        except ValueError:
            return 0

    return 0


def sort_by_id(elem):
    """Sort elements by ID if the 'id' attribute can be cast to an int."""
    id = elem.get('Id')
    if id:
        try:
            return int(id)
        except ValueError:
            return 0

    return 0


def sort_by_text(elem):
    """Sort XML elements by their text contents."""
    text = elem.text
    if text:
        return text
    else:
        return ''


def sort_attributes(item, sorted_item, reverse_flag=False):
    """Sort XML attributes alphabetically by key.

    The original item is left unmodified and its attributes are copied to the provided `sorted_item`.
    """
    attribute_keys = sorted(item.keys(), reverse=reverse_flag)
    for key in attribute_keys:
        sorted_item.set(key, item.get(key))


def sort_elements(items, new_element):
    items = sorted(items, key=attrgetter('tag'))
    for item in items:
        new_item = le.Element(item.tag)
        if item.text and item.text.isspace() is False:
            new_item.text = item.text
        sort_attributes(item, new_item, False)
        sort_elements(list(item), new_item)
        new_element.append(new_item)


def sort_xml_file(origin_input_xml_file, sorted_output_xml_file):
    with open(origin_input_xml_file, 'r') as (original):
        input_xml_doc = le.parse(original)
        input_xml_root = input_xml_doc.getroot()
        output_xml_root = le.Element(input_xml_root.tag, nsmap=input_xml_root.nsmap)
        sort_attributes(input_xml_root, output_xml_root)
        sort_elements(list(input_xml_root), output_xml_root)
        output_xml_tree = le.ElementTree(output_xml_root)
        with open(sorted_output_xml_file, 'wb') as (output_file):
            output_xml_tree.write(output_file, pretty_print=True)


def sort_xml_content(origin_input_xml_content):
    input_xml_doc = le.fromstring(origin_input_xml_content)
    input_xml_root = input_xml_doc
    output_xml_root = le.Element(input_xml_root.tag, nsmap=input_xml_root.nsmap)
    sort_attributes(input_xml_root, output_xml_root)
    sort_elements(list(input_xml_root), output_xml_root)
    output_xml_tree = le.ElementTree(output_xml_root)
    sorted_output_xml_content = le.tostring(output_xml_tree, pretty_print=True, encoding='utf-8')
    return sorted_output_xml_content