# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/tables/sql_lookup_table.py
# Compiled at: 2012-10-12 07:02:39
import logging, inspect, yaml, uuid
from coils.foundation import *
from coils.core import *
from table import Table

class SQLLookupTable(Table):

    def __init__(self, context=None, process=None, scope=None):
        """
        ctor
        
        :param context: Security and operation context for message lookup
        :param process: Proccess to use when resolving message lookup
        :param scope: Scope to use when resolving message lookup
        """
        Table.__init__(self, context=context, process=process, scope=scope)
        self._db = None
        self._cache = None
        self._hits = 0
        self._debug = False
        self._do_input_upper = False
        self._do_input_strip = False
        self._do_output_upper = False
        self._do_output_strip = False
        self.log = logging.getLogger('OIE.SQLLookupTable')
        return

    def __repr__(self):
        return ('<SQLLookupTable name="{0}" dataSource="{1}"/>').format(self.name, self.c['SQLDataSourceName'])

    def set_description(self, description):
        self.c = description
        if self.c.get('useSessionCache', True):
            self._cache = {}
        if self.c.get('enableDebug', False):
            self._debug = True
        if self.c.get('doInputUpper', False):
            self._do_input_upper = True
        if self.c.get('doInputStrip', False):
            self._do_input_strip = True
        if self.c.get('doOutputUpper', False):
            self._do_output_upper = True
        if self.c.get('doOutputStrip', False):
            self._do_output_strip = True
        if self.c.get('chainedTable', None):
            self._chained_table = Table.Load(self.c['chainedTable'])
        else:
            self._chained_table = None
        return

    def lookup_value(self, *values):
        if not self._db:
            self._db = SQLConnectionFactory.Connect(self.c['SQLDataSourceName'])
        if self._do_input_upper or self._do_input_strip:
            tmp = []
            for value in values:
                if isinstance(value, basestring):
                    if self._do_input_upper:
                        value = value.upper()
                    if self._do_input_strip:
                        value = value.strip()
                tmp.append(value)

            values = tuple(tmp)
            tmp = None
        if self._cache:
            if values in self._cache:
                self._hits += 1
                return self._cache[values]
        if self._db:
            cursor = self._db.cursor()
            try:
                if self._debug:
                    self.log.debug(('Performing table looking via "{0}"').format(self.name))
                    self.log.debug(('Values: {0}').format(values))
                cursor.execute(self.c['SQLQueryText'], *values)
            except Exception, e:
                self.log.error(('SQL execute excetion in {0} performing "{1}"').format(self, self.c['SQLQueryText']))
                raise e

            record = cursor.fetchone()
            if record:
                if self._debug:
                    self.log.debug('SQL Query found matching records')
                result = unicode(record[0])
            else:
                if self._debug:
                    self.log.debug('SQL Query found 0 matching records')
                result = None
            cursor.close()
            if result is None and self._chained_table:
                if self._debug:
                    self.log.debug(('Passing lookup to chained table {0}').format(self._chained_table.name))
                result = self._chained_table.lookup_value(*values)
            if result:
                if isinstance(result, basestring):
                    if self._do_output_upper:
                        result = result.upper()
                    if self._do_output_strip:
                        result = result.strip()
            if self._cache is not None:
                self._cache[values] = result
            if self._debug:
                self.log.debug(('Returning: {0}').format(result))
            return result
        else:
            raise CoilsException(('SQLLookup table unable to establish connection to SQLDataSource "{0}"').format(self.c['SQLDataSourceName']))
            return