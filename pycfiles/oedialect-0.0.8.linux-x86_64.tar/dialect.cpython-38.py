# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/oedialect/dialect.py
# Compiled at: 2020-04-01 07:23:01
# Size of source mod 2**32: 17490 bytes
from sqlalchemy.dialects import postgresql
from sqlalchemy import util
from sqlalchemy.engine import reflection
from sqlalchemy.dialects.postgresql.base import PGExecutionContext
import shapely, geoalchemy2, logging, warnings
from oedialect import dbapi, compiler as oecomp
from oedialect.compiler import OEDDLCompiler, OECompiler
logger = logging.getLogger('sqlalchemy.dialects.postgresql')

class OEExecutionContext(PGExecutionContext):

    def fire_sequence(self, sequence, type_):
        seq = {'type':'sequence', 
         'sequence':sequence.name}
        if sequence.schema is not None:
            seq['schema'] = sequence.schema
        query = {'command':'advanced/search', 
         'type':'select', 
         'fields':[
          {'type':'function', 
           'function':'nextval', 
           'operands':[
            seq]}]}
        return self._execute_scalar(query, type_)

    @classmethod
    def _init_compiled(cls, dialect, connection, dbapi_connection, compiled, parameters):
        """Initialize execution context for a Compiled construct."""
        self = cls.__new__(cls)
        self.root_connection = connection
        self._dbapi_connection = dbapi_connection
        self.dialect = connection.dialect
        self.compiled = compiled
        if not compiled.can_execute:
            raise AssertionError
        else:
            self.execution_options = compiled.execution_options.union(connection._execution_options)
            self.result_column_struct = (
             compiled._result_columns, compiled._ordered_columns,
             compiled._textual_ordered_columns)
            self.unicode_statement = util.text_type(compiled)
            if not dialect.supports_unicode_statements:
                self.statement = self.unicode_statement.encode(self.dialect.encoding)
            else:
                self.statement = self.unicode_statement
            self.isinsert = compiled.isinsert
            self.isupdate = compiled.isupdate
            self.isdelete = compiled.isdelete
            self.is_text = compiled.isplaintext
            if not parameters:
                self.compiled_parameters = [
                 compiled.construct_params()]
            else:
                self.compiled_parameters = [compiled.construct_params(m, _group_number=grp) for grp, m in enumerate(parameters)]
                self.executemany = len(parameters) > 1
            self.cursor = self.create_cursor()
            if self.isinsert or self.isupdate or self.isdelete:
                self.is_crud = True
                self._is_explicit_returning = bool(compiled.statement._returning)
                self._is_implicit_returning = bool(compiled.returning and not compiled.statement._returning)
            if self.compiled.insert_prefetch or self.compiled.update_prefetch:
                if self.executemany:
                    self._process_executemany_defaults()
                else:
                    self._process_executesingle_defaults()
        processors = compiled._bind_processors
        parameters = []
        if dialect.positional:
            for compiled_params in self.compiled_parameters:
                param = []
                for key in self.compiled.positiontup:
                    if key in processors:
                        param.append(processors[key](compiled_params[key]))
                    else:
                        param.append(compiled_params[key])
                else:
                    parameters.append(dialect.execute_sequence_format(param))

        else:
            encode = not dialect.supports_unicode_statements
            for compiled_params in self.compiled_parameters:
                if encode:
                    param = dict(((
                     dialect._encoder(key)[0],
                     processors[key](compiled_params[key]) if key in processors else compiled_params[key]) for key in compiled_params))
                else:
                    param = dict(((
                     key,
                     processors[key](compiled_params[key]) if key in processors else compiled_params[key]) for key in compiled_params))
                parameters.append(param)
            else:
                self.parameters = dialect.execute_sequence_format(parameters)
                self.statement = compiled
                return self

    @classmethod
    def _init_ddl(cls, dialect, connection, dbapi_connection, compiled_ddl):
        self = cls.__new__(cls)
        self.root_connection = connection
        self._dbapi_connection = dbapi_connection
        self.dialect = connection.dialect
        self.compiled = compiled = compiled_ddl
        self.isddl = True
        self.execution_options = compiled.execution_options
        if connection._execution_options:
            self.execution_options = dict(self.execution_options)
            self.execution_options.update(connection._execution_options)
        else:
            if not dialect.supports_unicode_statements:
                self.unicode_statement = util.text_type(compiled)
                self.statement = dialect._encoder(self.unicode_statement)[0]
            else:
                self.statement = self.unicode_statement = util.text_type(compiled)
            self.cursor = self.create_cursor()
            self.compiled_parameters = []
            if dialect.positional:
                self.parameters = [
                 dialect.execute_sequence_format()]
            else:
                self.parameters = [{}]
        self.statement = compiled_ddl.string
        return self

    def get_insert_default(self, column):
        if column.primary_key:
            if column is column.table._autoincrement_column:
                if column.server_default:
                    if column.server_default.has_argument:
                        exc = {'command':'advanced/search', 
                         'type':'select', 
                         'fields':[
                          column.server_default.arg]}
                        return self._execute_scalar(exc, column.type)
                if not column.default is None:
                    if column.default.is_sequence:
                        if column.default.optional:
                            try:
                                seq_name = column._postgresql_seq_name
                            except AttributeError:
                                tab = column.table.name
                                col = column.name
                                tab = tab[0:29 + max(0, 29 - len(col))]
                                col = col[0:29 + max(0, 29 - len(tab))]
                                name = '%s_%s_seq' % (tab, col)
                                column._postgresql_seq_name = seq_name = name
                            else:
                                if column.table is not None:
                                    effective_schema = self.connection.schema_for_object(column.table)
                                else:
                                    effective_schema = None
                                seq = {'type':'sequence',  'sequence':seq_name}
                                if effective_schema is not None:
                                    seq['schema'] = effective_schema
                                exc = {'command':'advanced/search', 
                                 'type':'select', 
                                 'fields':[
                                  {'type':'function', 
                                   'function':'nextval', 
                                   'operands':[
                                    seq]}]}
                                return self._execute_scalar(exc, column.type)
        return super(PGExecutionContext, self).get_insert_default(column)

    @property
    def rowcount(self):
        return self.cursor.rowcount


class OEDialect(postgresql.psycopg2.PGDialect_psycopg2):
    ddl_compiler = OEDDLCompiler
    statement_compiler = OECompiler
    execution_ctx_cls = OEExecutionContext
    _supports_create_index_concurrently = False
    _supports_drop_index_concurrently = False
    supports_comments = False

    def __init__(self, *args, **kwargs):
        self._engine = None
        self.default_schema_name = 'model_draft'
        if kwargs.get('json_serializer') is not None:
            warnings.warn("Use of the keyword 'json_serializer' is not supported")
        kwargs['json_serializer'] = lambda x: x
        if kwargs.get('json_deserializer') is not None:
            warnings.warn("Use of the keyword 'json_serializer' is not supported")
        kwargs['json_deserializer'] = lambda x: x
        (super(OEDialect, self).__init__)(*args, **kwargs)
        self.dbapi = dbapi

    def initialize(self, connection):
        pass

    def _check_unicode_description(self, connection):
        return isinstance('x', sa_util.text_type)

    def _check_unicode_returns(self, connection, additional_tests=None):
        return True

    def _get_server_version_info(self, connection):
        return (9, 3)

    def execute_with_cursor--- This code section failed: ---

 L. 282         0  LOAD_FAST                'connection'
                2  LOAD_METHOD              connect
                4  CALL_METHOD_0         0  ''
                6  SETUP_WITH           62  'to 62'
                8  STORE_FAST               'conn'

 L. 283        10  LOAD_FAST                'conn'
               12  LOAD_ATTR                connection
               14  LOAD_METHOD              cursor
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'cursor'

 L. 284        20  SETUP_FINALLY        36  'to 36'

 L. 285        22  LOAD_FAST                'cursor'
               24  LOAD_METHOD              execute
               26  LOAD_FAST                'query'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'res'
               32  POP_BLOCK        
               34  BEGIN_FINALLY    
             36_0  COME_FROM_FINALLY    20  '20'

 L. 287        36  LOAD_FAST                'cursor'
               38  LOAD_METHOD              close
               40  CALL_METHOD_0         0  ''
               42  POP_TOP          
               44  END_FINALLY      

 L. 288        46  LOAD_FAST                'res'
               48  POP_BLOCK        
               50  ROT_TWO          
               52  BEGIN_FINALLY    
               54  WITH_CLEANUP_START
               56  WITH_CLEANUP_FINISH
               58  POP_FINALLY           0  ''
               60  RETURN_VALUE     
             62_0  COME_FROM_WITH        6  '6'
               62  WITH_CLEANUP_START
               64  WITH_CLEANUP_FINISH
               66  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 50

    def _get_default_schema_name(self, connection):
        pass

    def has_schema(self, connection, schema):
        return self.execute_with_cursor(connection, {'command':'advanced/has_schema',  'schema':schema})

    def has_table(self, connection, table_name, schema=None):
        query = {'table': table_name}
        if schema:
            query['schema'] = schema
        else:
            query['schema'] = oecomp.DEFAULT_SCHEMA
        query['command'] = 'advanced/has_table'
        return self.execute_with_cursor(connection, query)

    def has_sequence(self, connection, sequence_name, schema=None):
        query = {'sequence_name': sequence_name}
        if schema:
            query['schema'] = schema
        query['command'] = 'advanced/has_sequence'
        return self.execute_with_cursor(connection, query)

    def has_type(self, connection, type_name, schema=None):
        query = {'type_name': type_name}
        if schema:
            query['schema'] = schema
        query['command'] = 'advanced/has_type'
        return self.execute_with_cursor(connection, query)

    @reflection.cache
    def get_table_oid(self, connection, table_name, schema=None, **kw):
        raise NotImplementedError

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        query = dict(kw)
        query['command'] = 'advanced/get_schema_names'
        return self.execute_with_cursor(connection, query)

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        query = {}
        if schema:
            query['schema'] = schema
        query.update(kw)
        query['command'] = 'advanced/get_table_names'
        return self.execute_with_cursor(connection, query)

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        query = {}
        if schema:
            query['schema'] = schema
        query.update(kw)
        query['command'] = 'advanced/get_view_names'
        return self.execute_with_cursor(connection, query)

    @reflection.cache
    def get_view_definition--- This code section failed: ---

 L. 353         0  LOAD_STR                 'view_name'
                2  LOAD_FAST                'view_name'
                4  BUILD_MAP_1           1 
                6  STORE_FAST               'query'

 L. 354         8  LOAD_FAST                'schema'
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 355        12  LOAD_FAST                'schema'
               14  LOAD_FAST                'query'
               16  LOAD_STR                 'schema'
               18  STORE_SUBSCR     
             20_0  COME_FROM            10  '10'

 L. 356        20  LOAD_FAST                'query'
               22  LOAD_METHOD              update
               24  LOAD_FAST                'kw'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 357        30  LOAD_STR                 'advanced/get_view_definition'
               32  LOAD_FAST                'query'
               34  LOAD_STR                 'command'
               36  STORE_SUBSCR     

 L. 358        38  LOAD_FAST                'connection'
               40  LOAD_METHOD              connect
               42  CALL_METHOD_0         0  ''
               44  SETUP_WITH           76  'to 76'
               46  STORE_FAST               'conn'

 L. 359        48  LOAD_FAST                'conn'
               50  LOAD_ATTR                connection
               52  LOAD_METHOD              cursor
               54  CALL_METHOD_0         0  ''
               56  LOAD_METHOD              execute
               58  LOAD_FAST                'query'
               60  CALL_METHOD_1         1  ''
               62  POP_BLOCK        
               64  ROT_TWO          
               66  BEGIN_FINALLY    
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  POP_FINALLY           0  ''
               74  RETURN_VALUE     
             76_0  COME_FROM_WITH       44  '44'
               76  WITH_CLEANUP_START
               78  WITH_CLEANUP_FINISH
               80  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 64

    @reflection.cache
    def get_columns_raw(self, engine, table_name, schema=None, **kw):
        query = {'table': table_name}
        if schema:
            query['schema'] = schema
        query['info_cache'] = {v:'+'.join(k[1]) for k, v in kw['info_cache'].items() if k[0] == 'get_columns_raw' if k[0] == 'get_columns_raw'}
        query['command'] = 'advanced/get_columns'
        with engine.connect() as (conn):
            response = conn.connection.post('advanced/get_columns', query)
            content = response['content']
        return content

    def get_columns(self, engine, table_name, schema=None, **kw):
        content = (self.get_columns_raw)(engine, table_name, schema, **kw)
        rows = content['columns']
        domains = content['domains']
        enums = content['enums']
        columns = []
        for name, format_type, default, notnull, attnum, table_oid in rows:
            column_info = self._get_column_info(name, format_type, default, notnull, domains, enums, schema, None)
            columns.append(column_info)
        else:
            return columns

    @reflection.cache
    def get_pk_constraint--- This code section failed: ---

 L. 394         0  LOAD_STR                 'table'
                2  LOAD_GLOBAL              str
                4  LOAD_FAST                'table_name'
                6  CALL_FUNCTION_1       1  ''
                8  BUILD_MAP_1           1 
               10  STORE_FAST               'query'

 L. 395        12  LOAD_FAST                'schema'
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 396        16  LOAD_FAST                'schema'
               18  LOAD_FAST                'query'
               20  LOAD_STR                 'schema'
               22  STORE_SUBSCR     
             24_0  COME_FROM            14  '14'

 L. 397        24  LOAD_FAST                'connection'
               26  LOAD_METHOD              connect
               28  CALL_METHOD_0         0  ''
               30  SETUP_WITH           68  'to 68'
               32  STORE_FAST               'conn'

 L. 398        34  LOAD_FAST                'conn'
               36  LOAD_ATTR                connection
               38  LOAD_METHOD              post
               40  LOAD_STR                 'advanced/get_pk_constraint'
               42  LOAD_FAST                'query'
               44  CALL_METHOD_2         2  ''
               46  STORE_FAST               'val'

 L. 399        48  LOAD_FAST                'val'
               50  LOAD_STR                 'content'
               52  BINARY_SUBSCR    
               54  POP_BLOCK        
               56  ROT_TWO          
               58  BEGIN_FINALLY    
               60  WITH_CLEANUP_START
               62  WITH_CLEANUP_FINISH
               64  POP_FINALLY           0  ''
               66  RETURN_VALUE     
             68_0  COME_FROM_WITH       30  '30'
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 56

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, postgresql_ignore_search_path=False, **kw):
        query = {'table': table_name}
        if schema:
            query['schema'] = schema
        if postgresql_ignore_search_path:
            query['postgresql_ignore_search_path'] = postgresql_ignore_search_path
        query.update(kw)
        if 'info_cache' in query:
            del query['info_cache']
        query['command'] = 'advanced/get_foreign_keys'
        return self.execute_with_cursor(connection, query)

    @reflection.cache
    def get_indexes(self, connection, table_name, schema, **kw):
        query = {'table':table_name,  'schema':schema}
        query.update(kw)
        query['command'] = 'advanced/get_indexes'
        return self.execute_with_cursor(connection, query)

    @reflection.cache
    def get_unique_constraints--- This code section failed: ---

 L. 426         0  LOAD_STR                 'table'
                2  LOAD_FAST                'table_name'
                4  BUILD_MAP_1           1 
                6  STORE_FAST               'query'

 L. 427         8  LOAD_FAST                'schema'
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 428        12  LOAD_FAST                'schema'
               14  LOAD_FAST                'query'
               16  LOAD_STR                 'schema'
               18  STORE_SUBSCR     
             20_0  COME_FROM            10  '10'

 L. 429        20  LOAD_FAST                'query'
               22  LOAD_METHOD              update
               24  LOAD_FAST                'kw'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 430        30  LOAD_STR                 'info_cache'
               32  LOAD_FAST                'query'
               34  COMPARE_OP               in
               36  POP_JUMP_IF_FALSE    44  'to 44'

 L. 431        38  LOAD_FAST                'query'
               40  LOAD_STR                 'info_cache'
               42  DELETE_SUBSCR    
             44_0  COME_FROM            36  '36'

 L. 432        44  LOAD_FAST                'connection'
               46  LOAD_METHOD              connect
               48  CALL_METHOD_0         0  ''
               50  SETUP_WITH           88  'to 88'
               52  STORE_FAST               'conn'

 L. 433        54  LOAD_FAST                'conn'
               56  LOAD_ATTR                connection
               58  LOAD_METHOD              post
               60  LOAD_STR                 'advanced/get_unique_constraints'
               62  LOAD_FAST                'query'
               64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'val'

 L. 434        68  LOAD_FAST                'val'
               70  LOAD_STR                 'content'
               72  BINARY_SUBSCR    
               74  POP_BLOCK        
               76  ROT_TWO          
               78  BEGIN_FINALLY    
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  POP_FINALLY           0  ''
               86  RETURN_VALUE     
             88_0  COME_FROM_WITH       50  '50'
               88  WITH_CLEANUP_START
               90  WITH_CLEANUP_FINISH
               92  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 76

    def get_isolation_level(self, connection):
        query = {'command': 'advanced/get_isolation_level'}
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        val = cursor.fetchone()[0]
        return val.upper()

    def set_isolation_level(self, connection, level):
        query = {'command':'advanced/set_isolation_level', 
         'level':level}
        return self.execute_with_cursor(connection, query)

    def do_prepare_twophase(self, connection, xid):
        result = connection.connection.cursor().execute('advanced/do_prepare_twophase', {'xid': xid})

    def do_rollback_twophase(self, connection, xid, is_prepared=True, recover=False):
        result = connection.connection.post('advanced/do_rollback_twophase', {'xid':xid,  'is_prepared':is_prepared, 
         'recover':recover})

    def do_commit_twophase(self, connection, xid, is_prepared=True, recover=False):
        result = connection.connection.post('advanced/do_commit_twophase', {'xid':xid,  'is_prepared':is_prepared, 
         'recover':recover})

    def do_recover_twophase(self, connection):
        result = connection.connection.post('advanced/do_recover_twophase', {})
        return [row[0] for row in result]

    def on_connect(self):
        pass


orig_init_WKBElement = geoalchemy2.WKBElement.__init__

def init_WKBElement(self, data, *args, **kwargs):
    if isinstance(data, str):
        data = shapely.wkb.dumps(shapely.wkb.loads(data, hex=True))
    orig_init_WKBElement(self, data, *args, **kwargs)


geoalchemy2.WKBElement.__init__ = init_WKBElement