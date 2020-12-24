# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bqorm/__init__.py
# Compiled at: 2019-03-29 16:28:53
# Size of source mod 2**32: 9770 bytes
import csv, os, logging, gzip, pickle, random, pandas as pd
from google.cloud import bigquery
import bqorm.conversions
DEBUG = False
if DEBUG:
    logging.basicConfig(level=(logging.DEBUG))

def load(filename):
    if DEBUG:
        logging.debug('bqorm.load({})'.format(filename))
    with gzip.open(filename, 'rb') as (f):
        table_data = pickle.load(f)
    for key, value in table_data.items():
        logging.debug(key)

    table = BQTable(schema=(table_data['schema']), data=(table_data['data']))
    return table


def read_bq(table_ref, credentials=None, limit=10, schema_only=False, columns=None):
    if DEBUG:
        logging.debug('bqorm.read_bq({})'.format(table_ref))
    else:
        table = BQTable()
        if credentials:
            client = bigquery.Client.from_service_account_json(credentials)
        else:
            client = bigquery.Client()
        if isinstance(table_ref, bigquery.TableReference):
            table_ref = '{}.{}.{}'.format(table_ref.project, table_ref.dataset_id, table_ref.table_id)
        schema = client.get_table(bigquery.Table(table_ref=table_ref)).schema
        table.schema = schema
        selector = schema_only or (','.join(columns) if columns else '*')
        query = 'select {} from `{}`'.format(selector, table_ref)
        if limit:
            query += ' limit {}'.format(limit)
        job = client.query(query)
        row_iterator = job.result()
        rows = [row.values() for row in row_iterator]
        columns = _rows_to_columns(rows=rows, schema=schema)
        table.data = columns
    return table


def _rows_to_columns(rows, schema):
    if DEBUG:
        logging.debug('bqorm._rows_to_columns()')
    schema_len = len(schema)
    columns = [[] for n in range(schema_len)]
    for row in rows:
        if isinstance(row, dict):
            row = [row.get(field.name) for field in schema]
        else:
            row_len = len(row)
            if row_len > schema_len:
                row = row[:schema_len]
            elif row_len < schema_len:
                row += [None] * (schema_len - row_len)
        for index, value in enumerate(row):
            columns[index].append(value)

    return columns


def _columns_to_rows--- This code section failed: ---

 L.  86         0  LOAD_GLOBAL              DEBUG
                2  POP_JUMP_IF_FALSE    14  'to 14'

 L.  87         4  LOAD_GLOBAL              logging
                6  LOAD_METHOD              debug
                8  LOAD_STR                 'bqorm._columns_to_rows()'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
             14_0  COME_FROM             2  '2'

 L.  89        14  LOAD_DEREF               'columns'
               16  POP_JUMP_IF_TRUE     22  'to 22'

 L.  90        18  BUILD_LIST_0          0 
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L.  91        22  BUILD_LIST_0          0 
               24  STORE_FAST               'rows'

 L.  92        26  LOAD_GLOBAL              max
               28  LOAD_LISTCOMP            '<code_object <listcomp>>'
               30  LOAD_STR                 '_columns_to_rows.<locals>.<listcomp>'
               32  MAKE_FUNCTION_0          ''
               34  LOAD_DEREF               'columns'
               36  GET_ITER         
               38  CALL_FUNCTION_1       1  ''
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'max_col_len'

 L.  93        44  LOAD_FAST                'n'
               46  POP_JUMP_IF_FALSE    58  'to 58'

 L.  94        48  LOAD_GLOBAL              min
               50  LOAD_FAST                'n'
               52  LOAD_FAST                'max_col_len'
               54  CALL_FUNCTION_2       2  ''
               56  STORE_FAST               'max_col_len'
             58_0  COME_FROM            46  '46'

 L.  96        58  LOAD_FAST                'row_type'
               60  LOAD_STR                 'list'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE   114  'to 114'

 L.  97        66  SETUP_LOOP          174  'to 174'
               68  LOAD_GLOBAL              range
               70  LOAD_FAST                'max_col_len'
               72  CALL_FUNCTION_1       1  ''
               74  GET_ITER         
               76  FOR_ITER            110  'to 110'
               78  STORE_DEREF              'index'

 L.  98        80  LOAD_CLOSURE             'index'
               82  BUILD_TUPLE_1         1 
               84  LOAD_LISTCOMP            '<code_object <listcomp>>'
               86  LOAD_STR                 '_columns_to_rows.<locals>.<listcomp>'
               88  MAKE_FUNCTION_8          'closure'
               90  LOAD_DEREF               'columns'
               92  GET_ITER         
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'row'

 L.  99        98  LOAD_FAST                'rows'
              100  LOAD_METHOD              append
              102  LOAD_FAST                'row'
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
              108  JUMP_BACK            76  'to 76'
              110  POP_BLOCK        
              112  JUMP_FORWARD        174  'to 174'
            114_0  COME_FROM            64  '64'

 L. 100       114  LOAD_FAST                'row_type'
              116  LOAD_STR                 'dict'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   174  'to 174'

 L. 101       122  SETUP_LOOP          174  'to 174'
              124  LOAD_GLOBAL              range
              126  LOAD_FAST                'max_col_len'
              128  CALL_FUNCTION_1       1  ''
              130  GET_ITER         
              132  FOR_ITER            172  'to 172'
              134  STORE_DEREF              'index'

 L. 102       136  LOAD_CLOSURE             'columns'
              138  LOAD_CLOSURE             'index'
              140  BUILD_TUPLE_2         2 
              142  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              144  LOAD_STR                 '_columns_to_rows.<locals>.<dictcomp>'
              146  MAKE_FUNCTION_8          'closure'
              148  LOAD_GLOBAL              enumerate
              150  LOAD_FAST                'schema'
              152  CALL_FUNCTION_1       1  ''
              154  GET_ITER         
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'row'

 L. 103       160  LOAD_FAST                'rows'
              162  LOAD_METHOD              append
              164  LOAD_FAST                'row'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          
              170  JUMP_BACK           132  'to 132'
              172  POP_BLOCK        
            174_0  COME_FROM_LOOP      122  '122'
            174_1  COME_FROM           120  '120'
            174_2  COME_FROM           112  '112'
            174_3  COME_FROM_LOOP       66  '66'

 L. 104       174  LOAD_FAST                'rows'
              176  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 174_3


class BQTable(object):

    def __init__(self, schema=None, data=None):
        if DEBUG:
            logging.debug('bqorm.BQTable.__init__')
        self.schema = schema if schema else []
        self.data = data if data else []

    def __eq__(self, other):
        return self.schema == other.schema and self.data == other.data

    def __setattr__(self, name, value):
        if DEBUG:
            logging.debug('bqorm.BQTable.set {}'.format(name))
        elif name == 'schema':
            self._set_schema(value)
        elif name == 'data':
            self._set_data(value)

    def __getattr__(self, name):
        if DEBUG:
            logging.debug('bqorm.BQTable.get {}'.format(name))
        if name == 'schema':
            return self._schema
        if name == 'data':
            return self._data

    def _set_schema(self, schema):
        if DEBUG:
            logging.debug('bqorm.BQTable._set_schema()')
        new_schema = []
        for field in schema:
            if isinstance(field, bigquery.SchemaField):
                new_schema.append(field)
            else:
                if isinstance(field, (tuple, list)):
                    new_schema.append((bigquery.SchemaField)(*field))

        if self.schema and new_schema and new_schema != self.schema:
            data = self._move_columns(new_schema)
        else:
            data = self.data
        data = self._typecheck(schema=new_schema, data=data)
        object.__setattr__(self, '_schema', new_schema)
        object.__setattr__(self, '_data', data)

    def _set_data(self, data):
        if DEBUG:
            logging.debug('bqorm.BQTable._set_data()')
        if data:
            if isinstance(data, list):
                if isinstance(data[0], dict):
                    data = _rows_to_columns(data, self.schema)
        data = self._typecheck(data=data)
        object.__setattr__(self, '_data', data)

    def _move_columns(self, schema):
        if DEBUG:
            logging.debug('bqorm.BQTable._move_columns()')
        old_field_names = [field.name for field in self.schema]
        new_field_names = [field.name for field in schema]
        column_order = [old_field_names.index(name) for name in new_field_names]
        return [self.data[index] for index in column_order]

    def _rename_columns(self, mapping):
        if DEBUG:
            logging.debug('bqorm.BQTable._rename_columns()')
        new_schema = [field for field in self.schema]
        old_field_names = [field.name for field in self.schema]
        for old_field_name, new_field_name in mapping.items():
            index = old_field_names.index(old_field_name)
            field = new_schema[index]
            new_schema[index] = bigquery.SchemaField(name=new_field_name,
              field_type=(field.field_type),
              mode=(field.mode),
              description=(field.description),
              fields=(field.fields))

        self.schema = new_schema

    def _typecheck(self, schema=None, data=None):
        if DEBUG:
            logging.debug('bqorm.BQTable._typecheck()')
        schema = schema if schema else self.schema
        data = data if data else self.data
        if schema:
            if data:
                typechecked_columns = []
                for index, field in enumerate(schema):
                    typechecked_columns.append(bqorm.conversions.convert(data[index], field.field_type, field.mode))

                return typechecked_columns
        return data

    def rename(self, columns):
        if DEBUG:
            logging.debug('bqorm.BQTable.rename()')
        self._rename_columns(mapping=columns)

    def append(self, rows):
        append_columns = _rows_to_columns(rows, self.schema)
        data = self.data
        for index in range(len(data)):
            data[index] += append_columns[index]

        self.data = data

    def rows(self, n=None, row_type='list'):
        if DEBUG:
            logging.debug('bqorm.BQTable.rows()')
        rows = _columns_to_rows(columns=(self.data),
          schema=(self.schema),
          n=n,
          row_type=row_type)
        return rows

    def save(self, filename):
        if DEBUG:
            logging.debug('bqorm.BQTable.save()')
        schema_dicts = [{'name':field.name,  'field_type':field.field_type,  'mode':field.mode,  'description':field.description,  'fields':field.fields} for field in self.schema]
        table_data = {'schema':schema_dicts, 
         'data':self.data}
        with gzip.open(filename, 'wb') as (f):
            pickle.dump(table_data, f, pickle.HIGHEST_PROTOCOL)

    def to_df(self):
        if DEBUG:
            logging.debug('bqorm.BQTable.to_df()')
        data = {field.name:self.data[index] for index, field in enumerate(self.schema)}
        return pd.DataFrame(data)

    def to_bq(self, table_ref, credentials=None, mode='append'):
        if DEBUG:
            logging.debug('bqorm.BQTable.to_bq({})'.format(table_ref))
        elif credentials:
            client = bigquery.Client.from_service_account_json(credentials)
        else:
            client = bigquery.Client()
        if isinstance(table_ref, str):
            table_ref = bigquery.TableReference.from_string(table_ref)
        tmpfile = 'tmpfile_{}.csv'.format(random.randint(1000, 9999))
        self.to_csv(tmpfile, delimiter=',')
        job_config = bigquery.LoadJobConfig()
        job_config.autodetect = False
        job_config.create_disposition = 'CREATE_IF_NEEDED'
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.write_disposition = 'WRITE_TRUNCATE' if mode == 'overwrite' else 'WRITE_APPEND'
        job_config.schema = self.schema
        with open(tmpfile, 'rb') as (csv_file):
            load_job = client.load_table_from_file(csv_file,
              table_ref,
              job_config=job_config,
              job_id_prefix='load_table_from_file')
            load_job.result()
        os.remove(tmpfile)

    def to_csv(self, filename, delimiter=','):
        if DEBUG:
            logging.debug('bqorm.BQTable.to_csv({})'.format(filename))
        with open(filename, 'w', newline='') as (csv_file):
            writer = csv.writer(csv_file, delimiter=delimiter)
            writer.writerows(self.rows())