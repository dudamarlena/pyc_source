# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/trane/utils/table_meta.py
# Compiled at: 2018-04-02 11:42:10
# Size of source mod 2**32: 4001 bytes
import copy, json
__all__ = [
 'TableMeta']

class TableMeta(object):
    __doc__ = 'Meta data of a database table. Defines column name and column data type of a database. '
    SUPERTYPE = {}
    TYPE_CATEGORY = 'categorical'
    TYPE_BOOL = 'boolean'
    TYPE_ORDERED = 'ordered'
    SUPERTYPE['categorical'] = 'categorical'
    SUPERTYPE['boolean'] = 'categorical'
    SUPERTYPE['ordered'] = 'categorical'
    TYPE_TEXT = 'text'
    TYPE_INTEGER = 'integer'
    TYPE_FLOAT = 'float'
    SUPERTYPE['integer'] = 'number'
    SUPERTYPE['float'] = 'number'
    TYPE_TIME = 'datetime'
    TYPE_IDENTIFIER = 'id'
    TYPES = [
     TYPE_CATEGORY, TYPE_BOOL, TYPE_ORDERED, TYPE_TEXT,
     TYPE_INTEGER, TYPE_FLOAT, TYPE_TIME, TYPE_IDENTIFIER]

    def __init__(self, table_meta):
        """args:
            table_meta: a dict describe meta data of a database.
                https://hdi-project.github.io/MetaData.json/index

        """
        self.table_meta = table_meta.copy()
        self.all_columns = {}
        for table_id, table in enumerate(self.table_meta['tables']):
            for field_id, field in enumerate(table['fields']):
                self.all_columns[field['name']] = {'table_id': table_id, 
                 'field_id': field_id, 
                 'type': field['subtype'] if 'subtype' in field else field['type'], 
                 'properties': field['properties'] if 'properties' in field else None}

    def get_type(self, column_name):
        """Get the type of a column.

        args:
            column_name: str

        returns:
            str: column type

        """
        return self.all_columns[column_name]['type']

    def set_type(self, column_name, dtype):
        """Change the type of a column.

        args:
            column_name: str
            dtype: str in TYPES

        returns:
            None

        """
        self.all_columns[column_name]['type'] = dtype
        column_data = self.all_columns[column_name]
        try:
            del self.table_meta['tables'][column_data['table_id']]['fields'][column_data['field_id']]['type']
            del self.table_meta['tables'][column_data['table_id']]['fields'][column_data['field_id']]['subtype']
        except:
            pass

        if dtype in TableMeta.SUPERTYPE:
            self.table_meta['tables'][column_data['table_id']]['fields'][column_data['field_id']]['type'] = TableMeta.SUPERTYPE[dtype]
            self.table_meta['tables'][column_data['table_id']]['fields'][column_data['field_id']]['subtype'] = dtype
        else:
            self.table_meta['tables'][column_data['table_id']]['fields'][column_data['field_id']]['type'] = dtype

    def get_property(self, column_name, property_name):
        """Get column property.

        """
        return self.all_columns[column_name]['properties'][property_name]

    def get_columns(self):
        """Get all the column names.

        returns:
            list of str: column names

        """
        return self.all_columns.keys()

    def copy(self):
        """Make a deep copy of self.

        returns:
            TableMeta: a copy

        """
        return copy.deepcopy(self)

    def to_json(self):
        """Convert to json str

        returns:
            str: json str of self

        """
        return json.dumps(self.table_meta)

    def from_json(json_data):
        """Load from json str.

        args:
            json_data: json str

        returns:
            TableMeta

        """
        return TableMeta(json.loads(json_data))

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False