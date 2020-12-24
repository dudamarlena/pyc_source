# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\modules\xml_parser\xml_table_processor_helpers.py
# Compiled at: 2019-01-24 04:26:09
# Size of source mod 2**32: 7890 bytes
import logging, re, string, copy, datetime

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
        return


def extract_all_items_from_node(node, name):
    try:
        return node.findall(name)
    except Exception as e:
        logging.error('Error. ' + str(e))


def check_exists_node(node, paths):
    try:
        result_node = None
        for path in paths:
            result_node = recursive_navigate(node, path, 0)
            if result_node != None:
                break

        return result_node
    except Exception as e:
        logging.error('Error. ' + str(e))
        return


def convert_str():
    try:
        pass
    except Exception as e:
        pass


def convert_output_values(formats, values):
    try:
        output_values = []
        _value = ''
        for value in values:
            _value = copy.copy(value)
            for f in formats:
                index = 0
                if f.value == 1:
                    if _value == '':
                        _value = '0'
                    _value = float(re.sub('[^0-9.]', '', _value.replace(',', '.')))
                if f.value == 2:
                    pass
                if f.value == 3:
                    if _value == '':
                        _value = 0
                    _value = round(_value / 1000, 2)
                index += 1

            output_values.append(_value)

        t = 0
        return output_values
    except Exception as e:
        logging.error('Error. ' + str(e))
        return values


def extract_value_join(column, values):
    try:
        value = ''
        if column.extract_value_type.value == 0:
            for v in values:
                value += str(v)

        else:
            if column.extract_value_type.value == 1:
                index = 0
                for v in values:
                    value += str(v)
                    if index < len(values) - 1:
                        value += ' '
                    index += 1

            else:
                if column.extract_value_type.value == 2:
                    index = 0
                    for v in values:
                        value += str(v)
                        if index < len(values) - 1:
                            value += '\n'
                        index += 1

        return value
    except Exception as e:
        logging.error('Error. ' + str(e))
        return


def extract_data_from_extra_table_field(root, column):
    try:
        column_paths = column.value_paths
        value_attribute_name = column.value_attribute_name
        if column_paths != None:
            if len(column_paths) > 0:
                paths_to_values = []
                if len(column_paths) == 1:
                    paths_to_values = column_paths[0]
                else:
                    for column_path in column_paths:
                        result_path = check_exists_node(root, column_path)
                        if result_path != None:
                            paths_to_values = column_path
                            break

                values = []
                for path_value in paths_to_values:
                    node_value = recursive_navigate(root, path_value, 0)
                    if node_value != None:
                        value = node_value.get(value_attribute_name)
                        if value != None:
                            values.append(value)

                extracted_value = extract_value_join(column, values)
                return extracted_value
        return ''
    except Exception as e:
        logging.error('Error. ' + str(e))
        return ''


def extract_data_from_table_row(xml_row, column):
    try:
        extracted_value = ''
        column_paths = column.value_paths
        value_attribute_name = column.value_attribute_name
        if column_paths != None and len(column_paths) > 0:
            paths_to_values = []
            if len(column_paths) == 1:
                paths_to_values = column_paths[0]
            else:
                for column_path in column_paths:
                    result_path = check_exists_node(xml_row, column_path)
                    if result_path != None:
                        paths_to_values = column_path
                        break

            values = []
            for path_value in paths_to_values:
                if column.condition.is_multiple_values == False:
                    node_value = recursive_navigate(xml_row, path_value, 0)
                    if node_value != None:
                        value = node_value.get(value_attribute_name)
                        if value != None:
                            values.append(value)
                else:
                    node_values = extract_all_items_from_node(xml_row, path_value[0])
                    for node_value in node_values:
                        if node_value != None:
                            value = node_value.get(value_attribute_name)
                            if value != None:
                                values.append(value)

            if column.condition.output_value_formats != None:
                if len(column.condition.output_value_formats) > 0:
                    values = convert_output_values(column.condition.output_value_formats, values)
            extracted_value = extract_value_join(column, values)
        return extracted_value
    except Exception as e:
        logging.error('Error. ' + str(e))
        return ''