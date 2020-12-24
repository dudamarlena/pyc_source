# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\models\processing_tables\processing_table_models.py
# Compiled at: 2019-01-30 09:27:36
# Size of source mod 2**32: 7133 bytes
import logging
from enum import Enum

class ValueDataTypesCollection(Enum):
    SIMPLE_VALUE = 0
    GROUP_VALUE = 1
    ARRAY_VALUE = 2
    CONDITION_VALUE = 3


class ConvertTypesCollection(Enum):
    WITHOUT = 0
    ONLY_NUMBERS = 1
    DATE = 1


class ConditionTypesCollection:
    EQUAL = 0
    NOT_EQUAL = 1
    MORE_THAN = 2
    LESS_THAN = 3
    EXISTS = 4


class OutputValueTypesCollection(Enum):
    WITHOUT = 0
    ONLY_NUMBERS = 1
    DATE = 2
    MONEY_FORMAT = 3
    THOUSAND_FORMAT = 4


class ExtractValueTypesCollection(Enum):
    SINGLE = 0
    JOIN_VALUE = 1
    JOIN_LIST = 2


class ConditionValue:

    def __init__(self, path_to_condition, value_for_check_condition_attribute, path_to_value, value_attribute, convert_value_for_checking_type, convert_value_type, condition_logic, condition_equal_values, output_value_formats, is_multiple_values=False):
        try:
            self.path_to_condition = path_to_condition
            self.value_for_check_condition_attribute = value_for_check_condition_attribute
            self.path_to_value = path_to_value
            self.value_attribute = (value_attribute,)
            self.convert_value_for_checking_type = convert_value_for_checking_type
            self.convert_value_type = convert_value_type
            self.condition_logic = condition_logic
            self.condition_equal_values = condition_equal_values
            self.output_value_formats = output_value_formats
            self.is_multiple_values = is_multiple_values
        except Exception as e:
            logging.error('Error initialization. ' + str(e))


class ProcessingTableCell:

    def __init__(self, column):
        try:
            self.value = ''
            self.column = column
            self.index = column.index
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def convert_value(self, value):
        try:
            return value
        except Exception as e:
            logging.error('Error convert cell value. ' + str(e))

    def set_value(self, value):
        try:
            if self.column.output_value_type.value != 1:
                self.value = self.convert_value(value)
            else:
                self.value = value
        except Exception as e:
            logging.error('Error set value to cell. ' + str(e))


class ProcessingTableRow:

    def __init__(self, index, columns):
        try:
            self.index = index
            self.columns = columns
            self.cells = []
            self.is_root = False
            self.group_id = -1
            self.not_classificated = False
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def init_cells_by_columns(self):
        try:
            for column in self.columns:
                self.cells.append(ProcessingTableCell(column))

        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def set_cell_value_by_index(self, index, value):
        try:
            for cell in self.cells:
                if cell.column.index == index:
                    cell.value = value
                    return

        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def set_cells_styles(self, style):
        try:
            pass
        except Exception as e:
            logging.error('Error initialization. ' + str(e))


class ProcessingTableColumn:

    def __init__(self, index, title, name, value_paths, value_attribute_name, condition, extract_value_type, extra_table_field=False):
        try:
            self.title = title
            self.name = name
            self.index = index
            self.value_paths = value_paths
            self.value_attribute_name = value_attribute_name
            self.extract_value_type = extract_value_type
            self.condition = condition
            self.extra_table_field = extra_table_field
        except Exception as e:
            logging.error('Error initialization. ' + str(e))


class ProcessingTable:

    def __init__(self, title, root_path, table_path, show_title=True, hidden_columns_in_groups=[]):
        try:
            self.title = title
            self.show_title = show_title
            self.table_path = table_path
            self.root_path = root_path
            self.columns = []
            self.rows = []
            self.group_rows = []
            self.hidden_columns_in_groups = hidden_columns_in_groups
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def init_column(self, title, name, value_paths, value_attribute_name, condition, extract_value_type, extra_table_field=False):
        try:
            column_index = len(self.columns) + 1
            column = ProcessingTableColumn(column_index, title, name, value_paths, value_attribute_name, condition, extract_value_type, extra_table_field)
            self.columns.append(column)
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def group_rows_by_values(self, column):
        try:
            pass
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def init_row(self, index, columns):
        try:
            row = ProcessingTableRow(index, columns)
            row.init_cells_by_columns()
            self.rows.append(row)
            return self.rows[(len(self.rows) - 1)]
        except Exception as e:
            logging.error('Error initialization. ' + str(e))