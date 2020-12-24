# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\modules\xml_parser\xml_table_processor.py
# Compiled at: 2019-01-30 08:21:59
# Size of source mod 2**32: 2684 bytes
import logging, modules.xml_parser.xml_table_processor_helpers as xml_helpers, modules.group_data_modules.group_table_data as group_table_data

def recursive_navigate(node, paths, index):
    try:
        r = node
        for result in node.findall(paths[index]):
            if index < len(paths) - 1:
                return recursive_navigate(result, paths, index + 1)
            else:
                return result

        return
    except Exception as e:
        logging.error('Error. ' + str(e))


def recursive_node_navigate(node, paths, index):
    try:
        r = node
        for result in node.findall(paths[index]):
            if index < len(paths) - 1:
                return recursive_node_navigate(result, paths, index + 1)
            else:
                return node

        return
    except Exception as e:
        logging.error('Error. ' + str(e))


def extract_all_items_from_node(node, name):
    try:
        return node.findall(name)
    except Exception as e:
        logging.error('Error. ' + str(e))


def process_table_rows(root, table, xml_rows):
    try:
        index = 1
        for xml_row in xml_rows:
            row = table.init_row(index, table.columns)
            for column in table.columns:
                if column.extra_table_field == True:
                    value = xml_helpers.extract_data_from_extra_table_field(root, column)
                else:
                    value = xml_helpers.extract_data_from_table_row(xml_row, column)
                row.set_cell_value_by_index(column.index, value)

        return
    except Exception as e:
        logging.error('Error. ' + str(e))


def process_table(root, document):
    try:
        index = 0
        for table in document.xml_document_tables:
            paths = table.table_path
            last_element = paths[(len(paths) - 1)]
            xml_table_body_node = recursive_node_navigate(root, paths, 0)
            xml_table_body_rows = extract_all_items_from_node(xml_table_body_node, last_element)
            process_table_rows(root, table, xml_table_body_rows)
            table = group_table_data.group_data_table(table)
            document.xml_document_tables[index] = table
            index += 1

        return
    except Exception as e:
        logging.error('Error. ' + str(e))