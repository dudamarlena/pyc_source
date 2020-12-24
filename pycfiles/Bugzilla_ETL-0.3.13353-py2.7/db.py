# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\util\db.py
# Compiled at: 2013-12-18 14:05:11
from datetime import datetime
import subprocess
from pymysql import connect, InterfaceError
from . import struct
from .maths import Math
from .strings import expand_template
from .struct import nvl
from .cnv import CNV
from .logs import Log, Except
from .queries import Q
from .strings import indent
from .strings import outdent
from .files import File
DEBUG = False
MAX_BATCH_SIZE = 100
all_db = []

class DB(object):
    """

    """

    def __init__(self, settings, schema=None, preamble=None):
        """
        OVERRIDE THE settings.schema WITH THE schema PARAMETER
        preamble WILL BE USED TO ADD COMMENTS TO THE BEGINNING OF ALL SQL
        THE INTENT IS TO HELP ADMINISTRATORS ID THE SQL RUNNING ON THE DATABASE
        """
        if settings == None:
            return
        else:
            all_db.append(self)
            if isinstance(settings, DB):
                settings = settings.settings
            self.settings = settings.copy()
            self.settings.schema = nvl(schema, self.settings.schema, self.settings.database)
            preamble = nvl(preamble, self.settings.preamble)
            if preamble == None:
                self.preamble = ''
            else:
                self.preamble = indent(preamble, '# ').strip() + '\n'
            self.debug = nvl(self.settings.debug, DEBUG)
            self._open()
            return

    def _open(self):
        """ DO NOT USE THIS UNLESS YOU close() FIRST"""
        try:
            self.db = connect(host=self.settings.host, port=self.settings.port, user=nvl(self.settings.username, self.settings.user), passwd=nvl(self.settings.password, self.settings.passwd), db=nvl(self.settings.schema, self.settings.db), charset='utf8', use_unicode=True)
        except Exception as e:
            Log.error('Failure to connect', e)

        self.cursor = None
        self.partial_rollback = False
        self.transaction_level = 0
        self.backlog = []
        return

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, type, value, traceback):
        if isinstance(value, BaseException):
            try:
                try:
                    if self.cursor:
                        self.cursor.close()
                    self.cursor = None
                    self.rollback()
                except Exception as e:
                    Log.warning('can not rollback()', e)

            finally:
                self.close()

            return
        else:
            try:
                try:
                    self.commit()
                except Exception as e:
                    Log.warning('can not commit()', e)

            finally:
                self.close()

            return

    def transaction(self):
        """
        return not-started transaction (for with statement)
        """
        return Transaction(self)

    def begin(self):
        if self.transaction_level == 0:
            self.cursor = self.db.cursor()
        self.transaction_level += 1
        self.execute("SET TIME_ZONE='+00:00'")

    def close(self):
        if self.transaction_level > 0:
            Log.error('expecting commit() or rollback() before close')
        self.cursor = None
        try:
            try:
                self.db.close()
            except Exception as e:
                if e.message.find('Already closed') >= 0:
                    return
                Log.warning('can not close()', e)

        finally:
            all_db.remove(self)

        return

    def commit(self):
        try:
            self._execute_backlog()
        except Exception as e:
            try:
                self.rollback()
            except Exception:
                pass

            Log.error('Error while processing backlog', e)

        if self.transaction_level == 0:
            Log.error('No transaction has begun')
        elif self.transaction_level == 1:
            if self.partial_rollback:
                try:
                    self.rollback()
                except Exception:
                    pass

                Log.error('Commit after nested rollback is not allowed')
            else:
                if self.cursor:
                    self.cursor.close()
                self.cursor = None
                self.db.commit()
        self.transaction_level -= 1
        return

    def flush(self):
        try:
            self.commit()
        except Exception as e:
            Log.error('Can not flush', e)

        try:
            self.begin()
        except Exception as e:
            Log.error('Can not flush', e)

    def rollback(self):
        self.backlog = []
        if self.transaction_level == 0:
            Log.error('No transaction has begun')
        elif self.transaction_level == 1:
            self.transaction_level -= 1
            if self.cursor != None:
                self.cursor.close()
            self.cursor = None
            self.db.rollback()
        else:
            self.transaction_level -= 1
            self.partial_rollback = True
            Log.warning('Can not perform partial rollback!')
        return

    def call(self, proc_name, params):
        self._execute_backlog()
        params = [ struct.unwrap(v) for v in params ]
        try:
            self.cursor.callproc(proc_name, params)
            self.cursor.close()
            self.cursor = self.db.cursor()
        except Exception as e:
            Log.error('Problem calling procedure ' + proc_name, e)

    def query(self, sql, param=None):
        self._execute_backlog()
        try:
            old_cursor = self.cursor
            if not old_cursor:
                self.cursor = self.db.cursor()
                self.cursor.execute("SET TIME_ZONE='+00:00'")
                self.cursor.close()
                self.cursor = self.db.cursor()
            if param:
                sql = expand_template(sql, self.quote_param(param))
            sql = self.preamble + outdent(sql)
            if self.debug:
                Log.note('Execute SQL:\n{{sql}}', {'sql': indent(sql)})
                self.cursor.execute(sql)
            columns = [ utf8_to_unicode(d[0]) for d in nvl(self.cursor.description, []) ]
            fixed = [ [ utf8_to_unicode(c) for c in row ] for row in self.cursor ]
            result = CNV.table2list(columns, fixed)
            if not old_cursor:
                self.cursor.close()
                self.cursor = None
            return result
        except Exception as e:
            if isinstance(e, InterfaceError) or e.message.find('InterfaceError') >= 0:
                Log.error('Did you close the db connection?', e)
            Log.error('Problem executing SQL:\n' + indent(sql.strip()), e, offset=1)

        return

    def forall(self, sql, param=None, _execute=None):
        assert _execute
        num = 0
        self._execute_backlog()
        try:
            old_cursor = self.cursor
            if not old_cursor:
                self.cursor = self.db.cursor()
            if param:
                sql = expand_template(sql, self.quote_param(param))
            sql = self.preamble + outdent(sql)
            if self.debug:
                Log.note('Execute SQL:\n{{sql}}', {'sql': indent(sql)})
            self.cursor.execute(sql)
            columns = tuple([ utf8_to_unicode(d[0]) for d in self.cursor.description ])
            for r in self.cursor:
                num += 1
                _execute(struct.wrap(dict(zip(columns, [ utf8_to_unicode(c) for c in r ]))))

            if not old_cursor:
                self.cursor.close()
                self.cursor = None
        except Exception as e:
            Log.error('Problem executing SQL:\n' + indent(sql.strip()), e, offset=1)

        return num

    def execute(self, sql, param=None):
        if self.transaction_level == 0:
            Log.error('Expecting transaction to be started before issuing queries')
        if param:
            sql = expand_template(sql, self.quote_param(param))
        sql = outdent(sql)
        self.backlog.append(sql)
        if self.debug or len(self.backlog) >= MAX_BATCH_SIZE:
            self._execute_backlog()

    def execute_file(self, filename, param=None):
        content = File(filename).read()
        self.execute(content, param)

    @staticmethod
    def execute_sql(settings, sql, param=None):
        """EXECUTE MANY LINES OF SQL (FROM SQLDUMP FILE, MAYBE?"""
        if param:
            with DB(settings) as (temp):
                sql = expand_template(sql, temp.quote_param(param))
        args = [
         'mysql',
         ('-h{0}').format(settings.host),
         ('-u{0}').format(settings.username),
         ('-p{0}').format(settings.password),
         ('{0}').format(settings.schema)]
        proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1)
        if isinstance(sql, unicode):
            sql = sql.encode('utf-8')
        output, _ = proc.communicate(sql)
        if proc.returncode:
            if len(sql) > 10000:
                sql = '<' + unicode(len(sql)) + ' bytes of sql>'
            Log.error('Unable to execute sql: return code {{return_code}}, {{output}}:\n {{sql}}\n', {'sql': indent(sql), 
               'return_code': proc.returncode, 
               'output': output})

    @staticmethod
    def execute_file(settings, filename, param=None):
        sql = File(filename).read()
        DB.execute_sql(settings, sql, param)

    def _execute_backlog(self):
        if not self.backlog:
            return
        backlog, self.backlog = self.backlog, []
        if self.db.__module__.startswith('pymysql'):
            for b in backlog:
                sql = self.preamble + b
                try:
                    if self.debug:
                        Log.note('Execute SQL:\n{{sql|indent}}', {'sql': sql})
                    self.cursor.execute(b)
                except Exception as e:
                    Log.error('Can not execute sql:\n{{sql}}', {'sql': sql}, e)

            self.cursor.close()
            self.cursor = self.db.cursor()
        else:
            for i, g in Q.groupby(backlog, size=MAX_BATCH_SIZE):
                sql = self.preamble + (';\n').join(g)
                try:
                    if self.debug:
                        Log.note('Execute block of SQL:\n{{sql|indent}}', {'sql': sql})
                    self.cursor.execute(sql)
                    self.cursor.close()
                    self.cursor = self.db.cursor()
                except Exception as e:
                    Log.error('Problem executing SQL:\n{{sql}}', {'sql': indent(sql.strip())}, e, offset=1)

    def insert(self, table_name, record):
        keys = record.keys()
        try:
            command = 'INSERT INTO ' + self.quote_column(table_name) + '(' + (',').join([ self.quote_column(k) for k in keys ]) + ') VALUES (' + (',').join([ self.quote_value(record[k]) for k in keys ]) + ')'
            self.execute(command)
        except Exception as e:
            Log.error('problem with record: {{record}}', {'record': record}, e)

    def insert_new(self, table_name, candidate_key, new_record):
        candidate_key = struct.listwrap(candidate_key)
        condition = (' AND\n').join([ self.quote_column(k) + '=' + self.quote_value(new_record[k]) if new_record[k] != None else self.quote_column(k) + ' IS Null' for k in candidate_key ])
        command = 'INSERT INTO ' + self.quote_column(table_name) + ' (' + (',').join([ self.quote_column(k) for k in new_record.keys() ]) + ')\n' + 'SELECT a.* FROM (SELECT ' + (',').join([ self.quote_value(v) + ' ' + self.quote_column(k) for k, v in new_record.items() ]) + ' FROM DUAL) a\n' + 'LEFT JOIN ' + "(SELECT 'dummy' exist FROM " + self.quote_column(table_name) + ' WHERE ' + condition + ' LIMIT 1) b ON 1=1 WHERE exist IS Null'
        self.execute(command, {})
        return

    def insert_newlist(self, table_name, candidate_key, new_records):
        for r in new_records:
            self.insert_new(table_name, candidate_key, r)

    def insert_list(self, table_name, records):
        if not records:
            return
        keys = set()
        for r in records:
            keys |= set(r.keys())

        keys = Q.sort(keys)
        try:
            command = 'INSERT INTO ' + self.quote_column(table_name) + '(' + (',').join([ self.quote_column(k) for k in keys ]) + ') VALUES ' + (',').join([ '(' + (',').join([ self.quote_value(r[k]) for k in keys ]) + ')' for r in records
                                                                                                                                                           ])
            self.execute(command)
        except Exception as e:
            Log.error('problem with record: {{record}}', {'record': records}, e)

    def update(self, table_name, where_slice, new_values):
        """
        where_slice IS A Struct WHICH WILL BE USED TO MATCH ALL IN table
        """
        new_values = self.quote_param(new_values)
        where_clause = (' AND\n').join([ self.quote_column(k) + '=' + self.quote_value(v) if v != None else self.quote_column(k) + ' IS NULL' for k, v in where_slice.items()
                                       ])
        command = 'UPDATE ' + self.quote_column(table_name) + '\n' + 'SET ' + (',\n').join([ self.quote_column(k) + '=' + v for k, v in new_values.items() ]) + '\n' + 'WHERE ' + where_clause
        self.execute(command, {})
        return

    def quote_param(self, param):
        return {k:self.quote_value(v) for k, v in param.items()}

    def quote_value(self, value):
        """
        convert values to mysql code for the same
        mostly delegate directly to the mysql lib, but some exceptions exist
        """
        try:
            if value == None:
                return 'NULL'
            else:
                if isinstance(value, SQL):
                    if not value.param:
                        return self.quote_sql(value.template)
                    param = {k:self.quote_sql(v) for k, v in value.param.items()}
                    return expand_template(value.template, param)
                if isinstance(value, basestring):
                    return self.db.literal(value)
                if isinstance(value, datetime):
                    return "str_to_date('" + value.strftime('%Y%m%d%H%M%S') + "', '%Y%m%d%H%i%s')"
                if hasattr(value, '__iter__'):
                    return self.db.literal(CNV.object2JSON(value))
                if isinstance(value, dict):
                    return self.db.literal(CNV.object2JSON(value))
                if Math.is_number(value):
                    return unicode(value)
                return self.db.literal(value)

        except Exception as e:
            Log.error('problem quoting SQL', e)

        return

    def quote_sql(self, value, param=None):
        """
        USED TO EXPAND THE PARAMETERS TO THE SQL() OBJECT
        """
        try:
            if isinstance(value, SQL):
                if not param:
                    return value
                param = {k:self.quote_sql(v) for k, v in param.items()}
                return expand_template(value, param)
            else:
                if isinstance(value, basestring):
                    return value
                if isinstance(value, dict):
                    return self.db.literal(CNV.object2JSON(value))
                if hasattr(value, '__iter__'):
                    return '(' + (',').join([ self.quote_sql(vv) for vv in value ]) + ')'
                return unicode(value)

        except Exception as e:
            Log.error('problem quoting SQL', e)

    def quote_column(self, column_name, table=None):
        if isinstance(column_name, basestring):
            if table:
                column_name = table + '.' + column_name
            return SQL('`' + column_name.replace('.', '`.`') + '`')
        else:
            if isinstance(column_name, list):
                if table:
                    return SQL((', ').join([ self.quote_column(table + '.' + c) for c in column_name ]))
                return SQL((', ').join([ self.quote_column(c) for c in column_name ]))
            return SQL(column_name.value + ' AS ' + self.quote_column(column_name.name))

    def sort2sqlorderby(self, sort):
        sort = Q.normalize_sort(sort)
        return (',\n').join([ self.quote_column(s.field) + (' DESC' if s.sort == -1 else ' ASC') for s in sort ])

    def esfilter2sqlwhere(self, esfilter):
        return SQL(self._filter2where(esfilter))

    def isolate(self, separator, list):
        if len(list) > 1:
            return '(\n' + indent((' ' + separator + '\n').join(list)) + '\n)'
        else:
            return list[0]

    def _filter2where(self, esfilter):
        esfilter = struct.wrap(esfilter)
        if esfilter['and']:
            return self.isolate('AND', [ self._filter2where(a) for a in esfilter['and'] ])
        if esfilter['or']:
            return self.isolate('OR', [ self._filter2where(a) for a in esfilter['or'] ])
        if esfilter['not']:
            return 'NOT (' + self._filter2where(esfilter['not']) + ')'
        else:
            if esfilter.term:
                return self.isolate('AND', [ self.quote_column(col) + '=' + self.quote_value(val) for col, val in esfilter.term.items() ])
            if esfilter.terms:
                for col, v in esfilter.terms.items():
                    try:
                        int_list = CNV.value2intlist(v)
                        has_null = False
                        for vv in v:
                            if vv == None:
                                has_null = True
                                break

                        if int_list:
                            filter = int_list_packer(col, int_list)
                            if has_null:
                                return self._filter2where({'or': [{'missing': col}, filter]})
                            return self._filter2where(filter)
                        else:
                            if has_null:
                                return self._filter2where({'missing': col})
                            else:
                                return 'false'

                    except Exception as e:
                        pass

                    return self.quote_column(col) + ' in (' + (', ').join([ self.quote_value(val) for val in v ]) + ')'

            else:
                if esfilter.script:
                    return '(' + esfilter.script + ')'
                if esfilter.range:
                    name2sign = {'gt': '>', 'gte': '>=', 
                       'lte': '<=', 
                       'lt': '<'}

                    def single(col, r):
                        min = nvl(r['gte'], r['>='])
                        max = nvl(r['lte'], r['<='])
                        if min and max:
                            return self.quote_column(col) + ' BETWEEN ' + self.quote_value(min) + ' AND ' + self.quote_value(max)
                        else:
                            return (' AND ').join(self.quote_column(col) + name2sign[sign] + self.quote_value(value) for sign, value in r.items())

                    output = self.isolate('AND', [ single(col, ranges) for col, ranges in esfilter.range.items() ])
                    return output
                if esfilter.missing:
                    if isinstance(esfilter.missing, basestring):
                        return '(' + self.quote_column(esfilter.missing) + ' IS Null)'
                    else:
                        return '(' + self.quote_column(esfilter.missing.field) + ' IS Null)'

                elif esfilter.exists:
                    if isinstance(esfilter.exists, basestring):
                        return '(' + self.quote_column(esfilter.exists) + ' IS NOT Null)'
                    else:
                        return '(' + self.quote_column(esfilter.exists.field) + ' IS NOT Null)'

                else:
                    Log.error('Can not convert esfilter to SQL: {{esfilter}}', {'esfilter': esfilter})
            return


def utf8_to_unicode(v):
    try:
        if isinstance(v, str):
            return v.decode('utf8')
        else:
            return v

    except Exception as e:
        Log.error('not expected', e)


class SQL(unicode):

    def __init__(self, template='', param=None):
        unicode.__init__(self)
        self.template = template
        self.param = param

    def __str__(self):
        Log.error('do not do this')


def int_list_packer(term, values):
    """
    return singletons, ranges and exclusions
    """
    DENSITY = 10
    MIN_RANGE = 20
    singletons = set()
    ranges = []
    exclude = set()
    sorted = Q.sort(values)
    last = sorted[0]
    curr_start = last
    curr_excl = set()
    for v in sorted[1:]:
        if v <= last + 1:
            pass
        elif v - last > 3:
            if last == curr_start:
                singletons.add(last)
            elif last - curr_start - len(curr_excl) < MIN_RANGE or last - curr_start < len(curr_excl) * DENSITY:
                singletons |= set(range(curr_start, last + 1))
                singletons -= curr_excl
            else:
                ranges.append({'gte': curr_start, 'lte': last})
                exclude |= curr_excl
            curr_start = v
            curr_excl = set()
        elif 1 + last - curr_start >= len(curr_excl) * DENSITY:
            add_me = set(range(last + 1, v))
            curr_excl |= add_me
        elif 1 + last - curr_start - len(curr_excl) < MIN_RANGE:
            new_singles = set(range(curr_start, last + 1)) - curr_excl
            singletons = singletons | new_singles
            curr_start = v
            curr_excl = set()
        else:
            ranges.append({'gte': curr_start, 'lte': last})
            exclude |= curr_excl
            curr_start = v
            curr_excl = set()
        last = v

    if last == curr_start:
        singletons.add(last)
    elif last - curr_start - len(curr_excl) < MIN_RANGE or last - curr_start < len(curr_excl) * DENSITY:
        singletons |= set(range(curr_start, last + 1))
        singletons -= curr_excl
    else:
        ranges.append({'gte': curr_start, 'lte': last})
        exclude |= curr_excl
    if ranges:
        r = {'or': [ {'range': {term: r}} for r in ranges ]}
        if exclude:
            r = {'and': [r, {'not': {'terms': {term: Q.sort(exclude)}}}]}
        if singletons:
            return {'or': [{'terms': {term: Q.sort(singletons)}},
                    r]}
        return r
    else:
        raise Except('no packing possible')


class Transaction(object):

    def __init__(self, db):
        self.db = db

    def __enter__(self):
        self.db.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.db.rollback()
        else:
            self.db.commit()