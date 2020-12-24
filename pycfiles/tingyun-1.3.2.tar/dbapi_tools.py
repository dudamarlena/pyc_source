# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/logistics/warehouse/dbapi_tools.py
# Compiled at: 2016-06-30 06:13:10
import re, weakref
_sql_parser_catch = weakref.WeakValueDictionary()
_parse_operation_p = '(\\w+)'
_parse_operation_re = re.compile(_parse_operation_p)
_identifier_re = re.compile('[\',"`\\[\\]\\(\\)]*')
_uncomment_sql_p = '/\\*.*?\\*/'
_uncomment_sql_re = re.compile(_uncomment_sql_p, re.DOTALL)
_normalize_params_1_p = '%\\([^)]*\\)s'
_normalize_params_1_re = re.compile(_normalize_params_1_p)
_normalize_params_2_p = '%s'
_normalize_params_2_re = re.compile(_normalize_params_2_p)
_normalize_params_3_p = ':\\w+'
_normalize_params_3_re = re.compile(_normalize_params_3_p)
_normalize_values_p = '\\([^)]+\\)'
_normalize_values_re = re.compile(_normalize_values_p)
_normalize_whitespace_1_p = '\\s+'
_normalize_whitespace_1_re = re.compile(_normalize_whitespace_1_p)
_normalize_whitespace_2_p = '\\s+(?!\\w)'
_normalize_whitespace_2_re = re.compile(_normalize_whitespace_2_p)
_normalize_whitespace_3_p = '(?<!\\w)\\s+'
_normalize_whitespace_3_re = re.compile(_normalize_whitespace_3_p)
_parse_identifier_1_p = '"((?:[^"]|"")+)"'
_parse_identifier_2_p = "'((?:[^']|'')+)'"
_parse_identifier_3_p = '`((?:[^`]|``)+)`'
_parse_identifier_4_p = '\\[\\s*(\\S+)\\s*\\]'
_parse_identifier_5_p = '\\(\\s*(\\S+)\\s*\\)'
_parse_identifier_6_p = '([^\\s\\(\\)\\[\\],]+)'
_parse_identifier_p = ('').join(('(', _parse_identifier_1_p, '|', _parse_identifier_2_p, '|', _parse_identifier_3_p, '|',
 _parse_identifier_4_p, '|', _parse_identifier_5_p, '|', _parse_identifier_6_p, ')'))
_parse_from_p = '\\s+FROM\\s+' + _parse_identifier_p
_parse_from_re = re.compile(_parse_from_p, re.IGNORECASE)
_parse_into_p = '\\s+INTO\\s+' + _parse_identifier_p
_parse_into_re = re.compile(_parse_into_p, re.IGNORECASE)
_parse_update_p = '\\s*UPDATE\\s+' + _parse_identifier_p
_parse_update_re = re.compile(_parse_update_p, re.IGNORECASE)
_parse_table_p = '\\s+TABLE\\s+' + _parse_identifier_p
_parse_table_re = re.compile(_parse_table_p, re.IGNORECASE)
_parse_call_p = '\\s*CALL\\s+(?!\\()(\\w+)'
_parse_call_re = re.compile(_parse_call_p, re.IGNORECASE)
_parse_show_p = '\\s*SHOW\\s+(.*)'
_parse_show_re = re.compile(_parse_show_p, re.IGNORECASE | re.DOTALL)
_parse_set_p = '\\s*SET\\s+(.*?)\\W+.*'
_parse_set_re = re.compile(_parse_set_p, re.IGNORECASE | re.DOTALL)
_parse_exec_p = '\\s*EXEC\\s+(?!\\()(\\w+)'
_parse_exec_re = re.compile(_parse_exec_p, re.IGNORECASE)
_parse_execute_p = '\\s*EXECUTE\\s+(?!\\()(\\w+)'
_parse_execute_re = re.compile(_parse_execute_p, re.IGNORECASE)
_parse_alter_p = '\\s*ALTER\\s+(?!\\()(\\w+)'
_parse_alter_re = re.compile(_parse_alter_p, re.IGNORECASE)
_int_re = re.compile('(?<!:)\\b\\d+\\b')
_single_quotes_p = "'(?:[^']|'')*'"
_double_quotes_p = '"(?:[^"]|"")*"'
_any_quotes_p = _single_quotes_p + '|' + _double_quotes_p
_single_quotes_re = re.compile(_single_quotes_p)
_double_quotes_re = re.compile(_double_quotes_p)
_any_quotes_re = re.compile(_any_quotes_p)
_quotes_default = _single_quotes_re
_quotes_table = {'MySQLdb': _any_quotes_re, 
   'pymysql': _any_quotes_re, 
   'oursql': _any_quotes_re}
plugin_db_mapping = {'MySQLdb': 'MySQL', 
   'cx_Oracle': 'Oracle'}
_explain_plan_table = {'MySQLdb': (
             'EXPLAIN', ('select', )), 
   'ibm_db_dbi': (
                'EXPLAIN', ('select', 'insert', 'update', 'delete')), 
   'oursql': (
            'EXPLAIN', ('select', )), 
   'pymysql': (
             'EXPLAIN', ('select', )), 
   'postgresql.interface.proboscis.engine2': (
                                            'EXPLAIN', ('select', 'insert', 'update', 'delete')), 
   'psycopg2': (
              'EXPLAIN', ('select', 'insert', 'update', 'delete')), 
   'psycopg2ct': (
                'EXPLAIN', ('select', 'insert', 'update', 'delete'))}

def _extract_identifier(token):
    return _identifier_re.sub('', token).strip().lower()


def _parse_default(sql, regex):
    match = regex.search(sql)
    return match and _extract_identifier(match.group(1)) or ''


def _parse_select(sql, engine):
    m = _parse_from_re.search(sql)
    return m and next(s for s in m.groups()[1:] if s).lower() or ''


def _parse_delete(sql, engine):
    m = _parse_from_re.search(sql)
    return m and next(s for s in m.groups()[1:] if s).lower() or ''


def _parse_insert(sql, engine):
    m = _parse_into_re.search(sql)
    return m and next(s for s in m.groups()[1:] if s).lower() or ''


def _parse_update(sql, engine):
    m = _parse_update_re.search(sql)
    return m and next(s for s in m.groups()[1:] if s).lower() or ''


def _parse_create(sql, engine):
    m = _parse_table_re.search(sql)
    return m and next(s for s in m.groups()[1:] if s).lower() or ''


def _parse_drop(sql, engine):
    m = _parse_table_re.search(sql)
    return m and next(s for s in m.groups()[1:] if s).lower() or ''


def _parse_call(sql, engine):
    return _parse_default(sql, _parse_call_re)


def _parse_show(sql, engine):
    return _parse_default(sql, _parse_show_re)


def _parse_set(sql, engine):
    return _parse_default(sql, _parse_set_re)


def _parse_exec(sql, engine):
    return _parse_default(sql, _parse_exec_re)


def _parse_execute(sql, engine):
    return _parse_default(sql, _parse_execute_re)


def _parse_alter(sql, engine):
    return _parse_default(sql, _parse_alter_re)


_operation_table = {'select': _parse_select, 
   'delete': _parse_delete, 
   'insert': _parse_insert, 
   'update': _parse_update, 
   'create': _parse_create, 
   'drop': _parse_drop, 
   'call': _parse_call, 
   'show': _parse_show, 
   'set': _parse_set, 
   'exec': _parse_exec, 
   'execute': _parse_execute, 
   'alter': _parse_alter}

def _parse_operation(sql, engine):
    match = _parse_operation_re.search(sql)
    operation = match and match.group(1).lower() or ''
    if operation in _operation_table:
        return operation
    return ''


def _parse_table(sql, engine, operation):
    parse = _operation_table.get(operation, None)
    return parse and parse(sql, engine) or ''


def _uncomment_sql(sql, engine):
    return _uncomment_sql_re.sub('', sql)


def _engine_name(engine):
    return engine and hasattr(engine, '__name__') and engine.__name__ or engine


def _obfuscate_sql(sql, engine=None):
    """
    :param sql:
    :param engine:
    :return:
    """
    name = _engine_name(engine)
    quotes_re = _quotes_table.get(name, _quotes_default)
    sql = quotes_re.sub('?', sql)
    sql = _int_re.sub('?', sql)
    return sql


def _normalize_sql(sql, engine):
    """
    :param sql:
    :param engine:
    :return:
    """
    sql = _normalize_params_1_re.sub('?', sql)
    sql = _normalize_values_re.sub('(?)', sql)
    sql = _normalize_params_2_re.sub('?', sql)
    sql = _normalize_params_3_re.sub('?', sql)
    sql = sql.strip()
    sql = _normalize_whitespace_1_re.sub(' ', sql)
    sql = _normalize_whitespace_2_re.sub('', sql)
    sql = _normalize_whitespace_3_re.sub('', sql)
    return sql


def _explain_plan(sql, engine, connect_params, cursor_params, execute_params):
    """
    :param sql:
    :param engine:
    :param connect_params:
    :param cursor_params:
    :param execute_params:
    :return:
    """
    if engine is None:
        return
    else:
        if type(engine) == type(''):
            return
        name = _engine_name(engine)
        if name is None:
            return
        if connect_params is None or cursor_params is None or execute_params is None:
            return
        if cursor_params is None:
            return
        if execute_params is None:
            return
        command, operations = _explain_plan_table.get(name, (None, None))
        if not command:
            return
        operation = _parse_operation(sql, engine)
        if operation not in operations:
            return
        query = '%s %s' % (command, sql)
        args, kwargs = connect_params
        try:
            connection = engine.connect(*args, **kwargs)
            try:
                args, kwargs = cursor_params
                cursor = connection.cursor(*args, **kwargs)
                try:
                    try:
                        args, kwargs = execute_params
                        cursor.execute(query, *args, **kwargs)
                        columns = []
                        if cursor.description:
                            for column in cursor.description:
                                columns.append(column[0])

                        rows = cursor.fetchall()
                        if not columns and not rows:
                            return
                        db_name = plugin_db_mapping.get(name, 'Unknown')
                        return {'dialect': db_name, 'keys': columns, 'values': [ [ str(t) for t in r ] for r in rows ]}
                    except Exception:
                        pass

                finally:
                    cursor.close()

            finally:
                try:
                    connection.rollback()
                except (AttributeError, engine.NotSupportedError):
                    pass

                connection.close()

        except Exception:
            pass

        return


class SQLParser(object):

    def __init__(self, sql, engine=None):
        self.sql = sql
        self.engine = engine
        self._operation = None
        self._table = None
        self._uncommented = None
        self._obfuscated = None
        self._normalized = None
        self._identifier = None
        return

    @property
    def operation(self):
        if self._operation is None:
            self._operation = _parse_operation(self.uncommented, self.engine)
        return self._operation

    @property
    def table(self):
        if self._table is None:
            self._table = _parse_table(self.uncommented, self.engine, self.operation)
        return str(self._table).split(';')[0]

    @property
    def uncommented(self):
        if self._uncommented is None:
            self._uncommented = _uncomment_sql(self.sql, self.engine)
        return self._uncommented

    @property
    def obfuscated(self):
        if self._obfuscated is None:
            self._obfuscated = _obfuscate_sql(self.uncommented, self.engine)
        return self._obfuscated

    @property
    def normalized(self):
        if self._normalized is None:
            self._normalized = _normalize_sql(self.obfuscated, self.engine)
        return self._normalized

    @property
    def identifier(self):
        if self._identifier is None:
            self._identifier = hash(self.normalized)
        return self._identifier

    def formatted(self, sql_format):
        if sql_format == 'off':
            return ''
        else:
            if sql_format == 'raw':
                return self.sql
            return self.obfuscated

    def explain_plan(self, connect_params, cursor_params, execute_params):
        """do sql explain.
        :param connect_params:
        :param cursor_params:
        :param execute_params:
        :return:
        """
        return _explain_plan(self.sql, self.engine, connect_params, cursor_params, execute_params)


def sql_parser(sql, engine):
    key = (
     sql, engine.__name__)
    result = _sql_parser_catch.get(key, None)
    if result is not None:
        return result
    else:
        result = SQLParser(sql, engine)
        _sql_parser_catch[key] = result
        return result