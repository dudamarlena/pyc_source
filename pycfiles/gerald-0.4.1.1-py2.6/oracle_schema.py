# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gerald/oracle_schema.py
# Compiled at: 2010-10-31 02:23:23
"""
Introduction
============
  Capture, document and manage Oracle database schemas.

  This is the Oracle Schema module. Every class in this module is subclassed 
  from the ones in the schema module. 

  A schema is comprised of collections of tables, views, stored code objects, 
  triggers, sequences (Oracle only), and other assorted 'objects'

  to create a new schema object from an existing database schema you will need 
  to do something like;

  >>> from gerald import OracleSchema
  >>> my_schema = OracleSchema('my_schema', 'oracle:/scott:tiger')

  If you don't specify a connection string you'll get an empty schema object.

  >>> from gerald import OracleSchema
  >>> my_schema = OracleSchema('my_schema')

Meta-Data
=========
  Module  : oracle_schema.py

  License : BSD License (see LICENSE.txt)

Known limitations
=================
  References to objects in other schemas are noted but are not properly 
  re-created e.g. if a table has a foreign key to another schema (indicated 
  by a value in R_OWNER on the USER_CONSTRAINTS table) this is not properly 
  generated.
  Will only work with the Oracle DB-API modules available in the dburi module,
  this is currently limited to cx_Oracle.
"""
__author__ = 'Andy Todd <andy47@halfcooked.com>'
__date__ = (2010, 1, 7)
__version__ = (0, 4, 1)
from gerald import schema
import sys
LOG = schema.LOG
TEXT_DATATYPES = [
 'CHAR', 'NCHAR', 'NVARCHAR2', 'VARCHAR2']
NUMERIC_DATATYPES = ['FLOAT', 'NUMBER']
DATE_DATATYPES = ['DATE', 'TIMESTAMP']
MISC_LENGTHLESS_DATATYPES = ['ROWID', 'UROWID', 'LONG', 'BLOB', 'CLOB', 'NCLOB', 'XMLTYPE']
DEFAULT_NUM_LENGTH = '38'
SYSTEM_SCHEMAS = ['MDSYS', 'TSMSYS', 'OUTLN', 'CTXSYS', 'FLOWS_FILES',
 'DBSNMP', 'XDB', 'SYS']

class Schema(schema.Schema):
    """
    A representation of an Oracle database schema

    An Oracle schema is all of the objects owned by a particular user
    """

    def _get_schema(self, cursor):
        """
        Get definitions for the objects in the current schema
        
        We query the data dictionary for (in order);
          - Tables, Views, Sequences, Code objects, DB links
        We should also get;
          - Grants and synonyms

        @param cursor: The cursor to use to query the data dictionary
        @type cursor: Database cursor object
        @return: All of the objects in this schema
        @rtype: Dictionary
        """
        LOG.info('Getting details for Oracle schema %s from database' % self.name)
        schema = {}
        stmt = 'SELECT user FROM dual'
        cursor.execute(stmt)
        schema_name = cursor.fetchone()[0]
        stmt = "SELECT table_name \n                  FROM   user_tables \n                  WHERE  table_name NOT LIKE 'DR%%'"
        cursor.execute(stmt)
        for table in cursor.fetchall():
            LOG.debug('Getting details for table %s' % table[0])
            self._set_unless_fail(schema, table[0], table[0], Table, cursor, schema_name)

        stmt = 'SELECT view_name\n                  FROM   user_views'
        cursor.execute(stmt)
        for view in cursor.fetchall():
            LOG.debug('Getting details for view %s' % view[0])
            self._set_unless_fail(schema, view[0], view[0], View, cursor, schema_name)

        stmt = 'SELECT sequence_name\n                  FROM   user_sequences'
        cursor.execute(stmt)
        for sequence in cursor.fetchall():
            LOG.debug('Getting details for sequence %s' % sequence[0])
            self._set_unless_fail(schema, sequence[0], sequence[0], Sequence, cursor, schema_name)

        stmt = "SELECT object_name, object_type\n                  FROM   user_objects\n                  WHERE  object_name IN (SELECT object_name FROM user_procedures)\n                  AND    object_type NOT IN ('PACKAGE BODY')\n                  "
        cursor.execute(stmt)
        for code_object in cursor.fetchall():
            (object_name, object_type) = code_object
            LOG.debug('Getting details for code object %s' % object_name)
            if object_type == 'PACKAGE':
                self._set_unless_fail(schema, object_name, object_name, Package, object_type, cursor, schema_name)
            else:
                schema[object_name] = CodeObject(object_name, object_type, cursor, schema_name)

        stmt = 'SELECT db_link\n                  FROM   user_db_links\n                  WHERE  password IS NOT NULL\n                  '
        cursor.execute(stmt)
        for db_link in cursor.fetchall():
            link_name = db_link[0]
            LOG.debug('Getting details for db link %s' % link_name)
            self._set_unless_fail(schema, link_name, link_name, DatabaseLink, cursor, schema_name)

        LOG.info('Got details for schema %s' % self.name)
        return schema


class User(schema.Schema):
    """
    A representation of an Oracle database user 
    
    This will contain all of the objects the supplied user can access.
    """

    def _get_schema(self, cursor):
        """
        Get definitions for all of the objects our user can see
        
        We query the data dictionary for (in order);
          - Tables, Views, Sequences, Code objects, DB links
        We should also get;
          - Grants and synonyms

        Note that object keys are 'schema.name' in this Class
        Note also that we don't capture database links (yet)

        @param cursor: The cursor to use to query the data dictionary
        @type cursor: Database cursor object
        @return: All of the objects in this schema
        @rtype: Dictionary
        """
        LOG.info('Getting details for Oracle user %s from database' % self.name)
        schema = {}
        stmt = "SELECT owner, table_name \n                  FROM   all_tables \n                  WHERE  table_name NOT LIKE 'DR%%'\n                  AND    owner NOT IN ('%s')\n               " % (',').join(SYSTEM_SCHEMAS)
        cursor.execute(stmt)
        for table in cursor.fetchall():
            (owner, table_name) = table
            LOG.debug('Getting details for table %s' % table_name)
            table_key = '%s.%s' % (owner, table_name)
            self._set_unless_fail(schema, table_key, table_name, Table, cursor, owner)

        stmt = 'SELECT view_name, owner\n                  FROM   all_views'
        cursor.execute(stmt)
        for view in cursor.fetchall():
            (view_name, owner) = view
            LOG.debug('Getting details for view %s' % view_name)
            view_key = '%s.%s' % (owner, view_name)
            self._set_unless_fail(schema, view_key, view_name, View, cursor, owner)

        stmt = 'SELECT sequence_name, sequence_owner\n                  FROM   all_sequences'
        cursor.execute(stmt)
        for seq in cursor.fetchall():
            (sequence, owner) = seq
            LOG.debug('Getting details for sequence %s' % sequence)
            sequence_key = '%s.%s' % (owner, sequence)
            self._set_unless_fail(schema, sequence_key, sequence, Sequence, cursor, owner)

        stmt = "SELECT object_name, object_type, owner\n                  FROM   all_objects\n                  WHERE  object_name IN (SELECT object_name FROM all_procedures)\n                  AND    object_type NOT IN ('PACKAGE BODY')\n               "
        cursor.execute(stmt)
        for code_object in cursor.fetchall():
            (object_name, object_type, owner) = code_object
            object_key = '%s.%s' % (owner, object_name)
            LOG.debug('Getting details for code object %s' % object_key)
            if object_type == 'PACKAGE':
                self._set_unless_fail(schema, object_key, object_name, Package, object_type, cursor, owner)
            else:
                self._set_unless_fail(schema, object_key, object_name, CodeObject, object_type, cursor, owner)

        LOG.info('Got details for user %s' % self.name)
        return schema


class OracleCalcPrecisionMixin(object):
    """Class to contain the calc_precision static method to be used as a 
    mixin by other classes in this module.
    """

    def calc_precision(data_type, data_length, data_precision=None, data_scale=None):
        """
        Calculate and then return the precision of this column
        
        This is a bit of a hack and will be replaced when columns become 
        first class objects.

        @param data_type: The data type of the column
        @type data_type: String
        @param data_length: The length of the column, if this is present its 
        usually the only numeric value provided
        @type data_length: Integer
        @param data_precision: The total number of digits in the column
        (optional)
        @type data_precision: Integer
        @param data_scale: The number of digits after the decimal point (optional)
        @type data_scale: Integer
        @return: The appropriate precision values for this column
        @rtype: String
        """
        if data_type in DATE_DATATYPES or data_type in MISC_LENGTHLESS_DATATYPES:
            precision = ''
        elif data_type in TEXT_DATATYPES:
            if data_length > 0:
                precision = '(%d)' % int(data_length)
            else:
                raise ValueError, 'Data length must be greater than zero'
        elif data_type in NUMERIC_DATATYPES:
            if data_precision:
                precision = '(' + str(int(data_precision))
                if data_scale:
                    precision += ',' + str(int(data_scale))
                precision += ')'
            else:
                precision = '(' + DEFAULT_NUM_LENGTH + ')'
        else:
            raise ValueError, 'Unknown data type'
        return precision

    calc_precision = staticmethod(calc_precision)


class OracleTableViewMixin(object):
    """Holder for a few code items common to both Tables and Views in Oracle."""

    def get_comments(self, cursor):
        uc_name = self.caseCorrectedName(self.name)
        stmt = 'SELECT comments\n                  FROM   all_tab_comments\n                  WHERE  table_name = :name\n                  AND    owner = :schema_name\n                  AND    comments IS NOT NULL'
        cursor.execute(stmt, (uc_name, self.schema))
        results = cursor.fetchall()
        if len(results) > 0:
            LOG.debug('Getting comments for %s' % uc_name)
            self.comments = results[0][0]

    def caseCorrectedName(self, name):
        if name.find('"') != -1:
            return name.strip('"')
        else:
            return name.upper()


class Table(schema.Table, OracleCalcPrecisionMixin, OracleTableViewMixin):
    """
    A representation of a database table.
    
    A table is made up of columns and will have indexes, triggers, primary keys 
    and foreign keys.
    """

    def _get_table(self, cursor):
        """
        Query the data dictionary for this table
        
        @param cursor: All of the select statements will be executed using this
          cursor.
        @type cursor: Database cursor object
        """
        uc_table_name = self.caseCorrectedName(self.name)
        stmt = 'SELECT tablespace_name\n                  FROM   all_tables\n                  WHERE  table_name = :table_name\n                  AND    owner = :schema_name'
        cursor.execute(stmt, (uc_table_name, self.schema))
        LOG.debug('Getting tablespace for table %s' % uc_table_name)
        result = cursor.fetchone()
        if result is None:
            raise AttributeError, "Can't get DDL for table %s" % uc_table_name
        self.tablespace_name = result[0]
        self.get_comments(cursor)
        stmt = 'SELECT utc.column_id, utc.column_name, utc.data_type, \n                         utc.data_length, utc.data_precision, utc.data_scale,\n                         utc.nullable, utc.data_default, ucc.comments\n                  FROM   all_tab_columns utc\n                         LEFT OUTER JOIN all_col_comments ucc ON \n                           (utc.table_name = ucc.table_name AND\n                            utc.column_name = ucc.column_name AND\n                            utc.owner = ucc.owner)\n                  WHERE  utc.table_name = :table_name\n                  AND    utc.owner = :schema_name'
        cursor.execute(stmt, (uc_table_name, self.schema))
        LOG.debug('Getting columns for table %s' % uc_table_name)
        for row in cursor.fetchall():
            column = {'name': row[1]}
            column['sequence'] = row[0]
            data_type = row[2]
            column['type'] = data_type
            if row[6] == 'Y':
                column['nullable'] = True
            else:
                column['nullable'] = False
            if data_type not in DATE_DATATYPES and data_type not in MISC_LENGTHLESS_DATATYPES:
                column['length'] = row[3]
            if data_type in NUMERIC_DATATYPES:
                if row[4]:
                    column['precision'] = row[4]
                    column['scale'] = row[5]
            if row[7]:
                column['default'] = row[7]
            if row[8]:
                column['comment'] = row[8]
            self.columns[column['name']] = column

        stmt = "SELECT constraint_name, \n                         decode(constraint_type, 'C', 'Check', 'P', 'Primary',\n                                  'U', 'Unique', 'R', 'Foreign', \n                                  'V', 'View Check', 'O', 'View Read Only') \n                                  constraint_type,\n                         r_constraint_name, search_condition,\n                         decode(status, 'ENABLED', 'Y', 'DISABLED', 'N') status\n                  FROM   all_constraints\n                  WHERE  table_name = :table_name\n                  AND    owner = :schema_name"
        cursor.execute(stmt, (uc_table_name, self.schema))
        LOG.debug('Getting constraints for table %s' % uc_table_name)
        for key in cursor.fetchall():
            constraint = {'name': key[0], 'type': key[1]}
            LOG.debug('Getting details for %s which is a %s constraint' % (
             constraint['name'], constraint['type']))
            if key[4] == 'Y':
                constraint['enabled'] = True
            else:
                constraint['enabled'] = False
            if constraint['type'] in ('Foreign', 'Primary'):
                stmt = 'SELECT column_name\n                          FROM   all_cons_columns\n                          WHERE  table_name = :table_name\n                          AND    owner = :schema_name\n                          AND    constraint_name = :constraint_name\n                          ORDER BY position'
                cursor.execute(stmt, (uc_table_name, self.schema, constraint['name']))
                columns = []
                for column in cursor.fetchall():
                    columns.append(column[0])

                constraint['columns'] = columns
                if constraint['type'] == 'Foreign':
                    constraint['refpk'] = key[2]
                    LOG.debug('Getting reference constraint %s' % constraint['refpk'])
                    stmt = 'SELECT table_name\n                              FROM   all_constraints\n                              WHERE  constraint_name = :constraint_name'
                    cursor.execute(stmt, (constraint['refpk'],))
                    try:
                        foreign_table = cursor.fetchone()[0]
                    except TypeError:
                        LOG.info('Cannot resolve foreign key constraint %s' % constraint['refpk'])
                        foreign_table = None
                    else:
                        if foreign_table:
                            constraint['reftable'] = foreign_table
                            stmt = 'SELECT column_name\n                                  FROM   all_cons_columns\n                                  WHERE  table_name = :table_name\n                                  AND    constraint_name = :constraint_name\n                                  ORDER BY position'
                            cursor.execute(stmt, (constraint['reftable'], constraint['refpk']))
                            columns = []
                            for column in cursor.fetchall():
                                columns.append(column[0])

                            constraint['refcolumns'] = columns
            elif constraint['type'] == 'Check':
                if not constraint['name'].startswith('SYS_C'):
                    constraint['condition'] = key[3]
            self.constraints[constraint['name']] = constraint

        stmt = 'SELECT index_name, index_type, uniqueness\n                  FROM   all_indexes\n                  WHERE  table_name = :table_name\n                  AND    owner = :schema_name'
        cursor.execute(stmt, (uc_table_name, self.schema))
        LOG.debug('Getting indexes for table %s' % uc_table_name)
        for index in cursor.fetchall():
            index_name = index[0]
            if index_name in self.constraints.keys():
                continue
            index_dict = {'name': index_name, 'type': index[1]}
            if index[2] == 'UNIQUE':
                index_dict['unique'] = True
            else:
                index_dict['unique'] = False
            stmt = 'SELECT column_name\n                      FROM   all_ind_columns\n                      WHERE  table_name = :table_name\n                      AND    table_owner = :schema_name\n                      AND    index_name = :index_name\n                      ORDER BY column_position'
            cursor.execute(stmt, (uc_table_name, self.schema, index_name))
            index_dict['columns'] = []
            for column in cursor.fetchall():
                index_dict['columns'].append(column[0])

            self.indexes[index_name] = index_dict

        stmt = 'SELECT trigger_name, owner\n                  FROM   all_triggers\n                  WHERE  table_name = :table_name\n                  AND    table_owner = :schema_name'
        cursor.execute(stmt, (uc_table_name, self.schema))
        LOG.debug('Getting triggers for table %s' % uc_table_name)
        for (trigger_name, trigger_owner) in cursor.fetchall():
            self.triggers[trigger_name] = Trigger(trigger_name, cursor, trigger_owner)

        return

    def get_ddl(self):
        """
        Generate the DDL necessary to create this table in an Oracle database
        
        @return: DDL to create this table 
        @rtype: String
        """
        ddl_strings = [
         self._get_table_ddl()]
        ddl_strings.append(self._get_comments_ddl())
        ddl_strings.append(self._get_constraint_ddl())
        ddl_strings.append(self._get_index_ddl())
        ddl_strings.append(self._get_trigger_ddl())
        return ('').join(ddl_strings)

    def _get_table_ddl(self):
        """
        Generate the DDL necessary to create the table and its columns in an
        Oracle database.

        @return: Table DDL
        @rtype: String
        """
        if not hasattr(self, 'name') or self.name == None:
            raise AttributeError, "Can't generate DDL for a table without a name"
        ddl_strings = [
         'CREATE TABLE ' + self.name]
        in_columns = False
        deco_cols = [ (x['sequence'], x) for x in self.columns.values() ]
        deco_cols.sort()
        sorted_cols = [ col for (seq, col) in deco_cols ]
        for column in sorted_cols:
            if in_columns:
                ddl_strings.append('\n  ,')
            else:
                ddl_strings.append('\n ( ')
                in_columns = True
            ddl_strings.append(column['name'] + ' ' + column['type'])
            if 'precision' in column:
                ddl_strings.append(self.calc_precision(column['type'], column['length'], column['precision'], column['scale']))
            elif 'length' in column:
                ddl_strings.append(self.calc_precision(column['type'], column['length']))
            else:
                ddl_strings.append(column['type'])
            if 'default' in column:
                ddl_strings.append(' DEFAULT %s' % column['default'])
            if not column['nullable']:
                ddl_strings.append(' NOT NULL')

        if len(ddl_strings) > 1:
            ddl_strings.append(' )')
        if self.tablespace_name:
            ddl_strings.append('\n TABLESPACE %s' % self.tablespace_name)
        ddl_strings.append(';\n')
        return ('').join(ddl_strings)

    def _get_comments_ddl(self):
        """
        Return the DDL for all of the comments defined against the table and its columns

        @return: DDL to create table and column comments
        @rtype: String
        """
        ddl_strings = []
        if hasattr(self, 'comments'):
            LOG.debug('Generating comment DDL for %s' % self.name)
            ddl_strings.append("COMMENT ON TABLE %s IS '%s';\n" % (self.name, self.comments))
        else:
            LOG.debug('Not generating comment DDL for %s' % self.name)
        for column in self.columns.values():
            if 'comment' in column:
                ddl_strings.append("COMMENT ON COLUMN %s.%s IS '%s';\n" % (self.name, column['name'], column['comment']))

        return ('').join(ddl_strings)

    def _get_named_constraint_ddl(self, constraint_name):
        """
        Generate the DDL for the constraint named constraint_name

        @parameter constraint_name: The name of a constraint
        @type constraint_name: String
        @return: DDL to create a constraint
        @rtype: String
        """
        ddl_strings = []
        if constraint_name in self.constraints:
            constr = self.constraints[constraint_name]
            if constr['type'] != 'Check' or not constr['name'].startswith('SYS_C'):
                ddl_strings.append('ALTER TABLE %s ADD' % self.name)
                ddl_strings.append(' CONSTRAINT %s' % constr['name'])
                if constr['type'] == 'Check':
                    ddl_strings.append(' CHECK (%s) ' % constr['condition'])
            if constr['type'] == 'Primary':
                ddl_strings.append(' PRIMARY KEY (')
            elif constr['type'] == 'Foreign':
                ddl_strings.append(' FOREIGN KEY (')
            if constr['type'] == 'Primary' or constr['type'] == 'Foreign':
                ddl_strings.append((', ').join(constr['columns']))
                ddl_strings.append(')')
            if constr['type'] == 'Foreign':
                ddl_strings.append(' REFERENCES %s (' % constr['reftable'])
                ddl_strings.append((', ').join(constr['refcolumns']))
                ddl_strings.append(')')
            if constr['type'] != 'Check' or not constr['name'].startswith('SYS_C'):
                ddl_strings.append(';\n')
        return ('').join(ddl_strings)

    def _get_constraint_ddl(self):
        """
        Generate the DDL for all of the constraints defined against this table
        in Oracle database syntax.

        @return: DDL to create zero, one or more constraints
        @rtype: String
        """
        ddl_strings = []
        for constraint in self.constraints:
            ddl_strings.append(self._get_named_constraint_ddl(constraint))

        return ('').join(ddl_strings)

    def _get_index_ddl(self):
        """
        Generate the DDL necessary to create indexes defined against this table 
        in an Oracle database
        
        @return: DDL to create the indexes for this table 
        @rtype: String
        """
        ddl_strings = []
        for index in self.indexes:
            if not index.startswith('SYS'):
                index_details = self.indexes[index]
                ddl_strings.append('CREATE')
                if index_details['unique']:
                    ddl_strings.append(' UNIQUE')
                ddl_strings.append(' INDEX %s ON %s' % (index, self.name))
                ddl_strings.append(' ( %s );\n' % (',').join(index_details['columns']))

        return ('').join(ddl_strings)

    def _get_trigger_ddl(self):
        """
        Generate the DDL necessary to create any triggers defined against this
        table in an Oracle database.

        @return: DDL to create zero, one or more triggers
        @rtype: String
        """
        ddl_strings = []
        for trigger in self.triggers:
            ddl_strings.append('\n')
            ddl_strings.append(self.triggers[trigger].get_ddl())

        return ('').join(ddl_strings)


class View(schema.View, OracleCalcPrecisionMixin, OracleTableViewMixin):
    """
    A representation of a database view.

    A View is made up of columns and also has an associated SQL statement.
    
    Most of the methods for this class are inherited from schema.View
    """
    view_sql = {'text': 'SELECT text \n                 FROM all_views \n                 WHERE view_name=:name \n                 AND owner=:schema_name', 
       'columns': 'SELECT atc.column_id, atc.column_name, atc.data_type, atc.data_length,\n                           atc.data_precision, atc.data_scale, atc.nullable, acc.comments\n                    FROM   all_tab_columns atc\n                    LEFT OUTER JOIN all_col_comments acc ON \n                      (    atc.table_name = acc.table_name\n                       AND atc.column_name = acc.column_name\n                       AND atc.owner = acc.owner)\n                    WHERE  atc.table_name=:name\n                    AND    atc.owner=:schema_name', 
       'triggers': 'SELECT trigger_name \n                     FROM all_triggers \n                     WHERE table_name=:name\n                     AND table_owner=:schema_name'}

    def _get_view(self, cursor):
        """
        Query the data dictionary for this view

        @param cursor: All of the select statements will be executed using this
          cursor.
        @type cursor: Database cursor object
        """
        uc_view_name = self.caseCorrectedName(self.name)
        cursor.execute(self.view_sql['text'], (uc_view_name, self.schema))
        LOG.debug('Getting text for view %s' % uc_view_name)
        self.sql = cursor.fetchone()[0]
        cursor.execute(self.view_sql['columns'], (uc_view_name, self.schema))
        LOG.debug('Getting columns for view %s' % uc_view_name)
        for col_row in cursor.fetchall():
            col_name = col_row[1]
            column = {'sequence': col_row[0], 'name': col_name}
            column['type'] = col_row[2]
            column['length'] = col_row[3]
            column['precision'] = col_row[4]
            column['scale'] = col_row[5]
            if col_row[6] == 'Y':
                column['nullable'] = True
            else:
                column['nullable'] = False
            column['comment'] = col_row[7]
            self.columns[col_name] = column

        cursor.execute(self.view_sql['triggers'], (self.name, self.schema))
        LOG.debug('Getting triggers for index %s' % self.name)
        for trigger in cursor.fetchall():
            trigger_name = trigger[0]
            self.triggers[trigger_name] = Trigger(trigger_name, cursor, self.schema)

        self.get_comments(cursor)

    def get_ddl(self):
        """
        Generate the DDL necessary to create this view

        @return: DDL to create this view
        @rtype: String
        """
        if not hasattr(self, 'name') or self.name == None:
            raise AttributeError, "Can't generate DDL for a view without a name"
        ddl_strings = [
         'CREATE VIEW %s' % self.name]
        in_columns = False
        cols = self.columns.values()
        cols.sort()
        for column in cols:
            if in_columns:
                ddl_strings.append('\n ,')
            else:
                ddl_strings.append(' ( ')
                in_columns = True
            ddl_strings.append(column['name'] + ' ')

        if in_columns:
            ddl_strings.append(') AS\n  ')
        ddl_strings.append(self.sql)
        return ('').join(ddl_strings)


class Trigger(schema.Trigger):
    """
    A representation of a database trigger.

    A trigger has triggering events and a SQL statement. A trigger can only
    exist within the context of a table or view and thus doesn't need any table 
    references as you can get those from its parent. Apart from the table or 
    view name, of course, which we need for the get_ddl method.

    Most of the methods for this class are inherited from schema.Trigger
    """

    def _get_trigger(self, cursor):
        """
        Query the data dictionary for this trigger
        
        @param cursor: All of the select statements will be executed using this
          cursor.
        @type cursor: Database cursor object
        """
        stmt = 'SELECT trigger_type, triggering_event, \n                         trigger_body, table_name\n                  FROM   all_triggers\n                  WHERE  trigger_name = :name\n                  AND    owner = :schema'
        LOG.debug('Getting details for trigger %s' % self.name)
        cursor.execute(stmt, (self.name, self.schema))
        results = cursor.fetchone()
        (self.scope, events, self.sql, self.table_name) = results
        self.events = events.split(' OR ')
        if self.scope.endswith('EACH ROW'):
            self.scope = self.scope[:-9]
            self.level = 'row'
        else:
            self.scope = self.scope[:-10]
            self.level = 'statement'

    def get_ddl(self):
        """
        Generate the DDL necessary to create this trigger

        @return: DDL to create this trigger
        @rtype: String
        """
        if not self.scope or not self.level or len(self.events) == 0 or not self.sql:
            raise ValueError, 'Cannot generate ddl for trigger %s' % self.name
        ddl_strings = [
         'CREATE OR REPLACE TRIGGER %s' % self.name]
        ddl_strings.append(' %s ' % self.scope)
        ddl_strings.append('%s ON ' % (' OR ').join(self.events))
        ddl_strings.append('%s' % self.table_name)
        if self.level == 'row':
            ddl_strings.append(' FOR EACH ROW')
        ddl_strings.append(' ')
        ddl_strings.append(self.sql)
        return ('').join(ddl_strings)


class Sequence(schema.Sequence):
    """
    A representation of a database sequence.

    A sequence is an in memory construct that provides sequential numbers.
    They are generally used to generate primary key values.

    Most of the methods for this class are inherited from schema.Sequence
    """

    def _get_sequence(self, cursor):
        """
        Query the data dictionary for this sequence. 

        Until Oracle provides a way to determine the current value for a
        sequence without altering it curr_value will always be None.

        @param cursor: All of the select statements will be executed using this
          cursor.
        @type cursor: Database cursor object
        """
        stmt = 'SELECT min_value, max_value, increment_by\n                  FROM   all_sequences\n                  WHERE  sequence_name=:seqname\n                  AND    sequence_owner=:schema'
        LOG.debug('Getting details for sequence %s' % self.name)
        cursor.execute(stmt, (self.name.upper(), self.schema))
        results = cursor.fetchone()
        (self.min_value, self.max_value, self.increment_by) = results

    def get_ddl(self):
        """Produce the DDL necessary to create this sequence

        @return: DDL to create this sequence
        @rtype: String
        """
        ddl_strings = [
         'CREATE SEQUENCE ' + self.name]
        if hasattr(self, 'curr_value') and self.curr_value != None:
            ddl_strings.append(' START WITH %d' % self.curr_value)
        if hasattr(self, 'min_value') and self.min_value > 1:
            ddl_strings.append(' MINVALUE %d' % self.min_value)
        if hasattr(self, 'max_value') and self.max_value != None:
            try:
                max_value = int(self.max_value)
            except OverflowError:
                max_value = -1
            else:
                if max_value > 1:
                    ddl_strings.append(' MAXVALUE %d' % max_value)
        if hasattr(self, 'increment_by') and self.increment_by > 1:
            ddl_strings.append(' INCREMENT BY %d' % self.increment_by)
        ddl_strings.append(';\n')
        return ('').join(ddl_strings)


class CodeObject(schema.CodeObject):
    """
    A representation of a database stored code object.

    Most of the methods for this class are inherited from schema.CodeObject

    For Oracle databases stored procedures and functions will be represented by
    a CodeObject. Database packages have their own sub-class called Package.
    """

    def _get_code_object(self, cursor):
        """
        Query the data dictionary for this code object

        @param cursor: All of the select statements will be executed using this
          cursor.
        @type cursor: Database cursor object
        """
        if self.name.find('"') != -1:
            uc_object_name = self.name.strip('"')
        else:
            uc_object_name = self.name.upper()
        stmt = 'SELECT line, text \n                  FROM   all_source \n                  WHERE  name=:object_name\n                  AND    type=:object_type\n                  AND    owner=:schema\n                  ORDER BY line'
        cursor.execute(stmt, (uc_object_name, self.object_type, self.schema))
        LOG.debug('Getting source for code object %s' % self.name)
        self.source = []
        for code_line in cursor.fetchall():
            self.source.append(code_line)

        LOG.debug('Got %d lines of source code for code object %s' % (len(self.source), self.name))
        LOG.debug(self.source)
        if self.object_type == 'PACKAGE':
            cursor.execute(stmt, (uc_object_name, 'PACKAGE BODY'))
            LOG.debug('Getting body source for package %s' % self.name)
            self.body_source = []
            for code_line in cursor.fetchall():
                self.body_source.append(code_line)

    def get_ddl(self):
        """
        Produce the DDL necessary to create this code object

        @return: DDL to create this code object
        @rtype: String
        """
        if not self.source:
            return None
        else:
            ddl_strings = [
             'CREATE OR REPLACE ']
            ddl_strings.extend([ x[1] for x in self.source ])
            return ('').join(ddl_strings)


class Package(CodeObject):
    """
    A representation of a database stored code object.

    Most of the methods for this class are inherited from schema.CodeObject

    A key differentiator for Oracle is the Package. This is made up of a package
    header and a package body, each of which is a separate database object.
    These will have an extra attribute

      - body_source (does what it says on the tin)
    """

    def _get_code_object(self, cursor):
        """Query the data dictionary for this code object

        @param cursor: All of the select statements will be executed using this
          cursor.
        @type cursor: Database cursor object
        """
        if self.name.find('"') != -1:
            uc_object_name = self.name.strip('"')
        else:
            uc_object_name = self.name.upper()
        stmt = 'SELECT line, text \n                  FROM   all_source \n                  WHERE  name=:object_name\n                  AND    type=:object_type\n                  AND    owner=:schema\n                  ORDER BY line'
        LOG.debug('Getting source for package %s' % self.name)
        cursor.execute(stmt, (uc_object_name, self.object_type.upper(), self.schema))
        self.source = []
        for code_line in cursor.fetchall():
            self.source.append(code_line)

        cursor.execute(stmt, (uc_object_name, 'PACKAGE BODY', self.schema))
        LOG.debug('Getting body source for package %s' % self.name)
        self.body_source = []
        for code_line in cursor.fetchall():
            self.body_source.append(code_line)

    def get_body_ddl(self):
        """Produce the DDL for a package body

        @return: DDL to create a package body
        @rtype: String
        """
        if not self.body_source:
            return ''
        ddl_strings = [
         'CREATE OR REPLACE ']
        ddl_strings.extend([ x[1] for x in self.body_source ])
        return ('').join(ddl_strings)


class DatabaseLink(object):
    """A representation of a database link.

    A database link is a way of accessing objects from another database without
    having to create another connection.

    This is, to the best of my knowledge, an Oracle specific concept so there is
    no super class to inherit from. This means that this class implements all of
    the 'standard' methods for schema objects (get_ddl, dump, to_xml, compare, 
    etc.)

    A database link has two attributes;
      - name  
      - connection_string
    """

    def __init__(self, name, cursor=None, schema=None):
        """Initialise a database link object. If a value is passed into the
        cursor parameter then the last thing we do is call L{_get_database_link}.

        @param name: The name of this database link
        @type name: String
        @param cursor: When specified this is used to access the data dictionary for the details of this database link
        @type cursor: Database cursor object
        """
        self.name = name
        self.connection_string = None
        if schema:
            self.schema = schema
        else:
            self.schema = None
        if cursor:
            self._get_database_link(cursor)
        return

    def _get_database_link(self, cursor):
        """Get the details of this database link from the data dictionary.

        @param cursor: A database cursor
        @type cursor: Database cursor object
        """
        stmt = 'SELECT username, password, host\n                  FROM   all_db_links\n                  WHERE  db_link=:db_link_name\n                  AND    owner=:schema\n               '
        cursor.execute(stmt, db_link_name=self.name.upper(), schema=self.schema)
        LOG.debug('Getting details of database link %s' % self.name)
        results = cursor.fetchone()
        connection_string = ''
        if results[0]:
            connection_string = results[0] + '/' + results[1]
            if results[2]:
                connection_string += '@' + results[2]
        elif results[2]:
            connection_string = results[2]
        self.connection_string = connection_string

    def get_ddl(self):
        """Produce the DDL necessary to create this database link

        @return: DDL to create this database link
        @rtype: String
        """
        ddl_string = 'CREATE DATABASE LINK %s ' % self.name
        ddl_string += "USING '%s'" % self.connection_string
        return ddl_string

    def dump(self):
        """Return the structure of this database link 
        
        Preferably in a nice easy to read format.

        @return: A description of this database link
        @rtype: String
        """
        outputs = [
         'Database link : %s' % self.name]
        outputs.append('  connection string : %s' % self.connection_string)
        return ('\n').join(outputs)

    def to_xml(self):
        """Return the structure of this database link as an XML document 
        fragment

        This will be of the form::
          <database_link name="%s">
            <connection_string>%s</connection_string>
          </database_link>

        @return: An XML fragment describing this database link
        @rtype: String
        """
        xml_strings = [
         '<database_link name="%s">' % self.name]
        conn_string = '  <connection_string>%s' % self.connection_string
        conn_string += '</connection_string>'
        xml_strings.append(conn_string)
        xml_strings.append('</database_link>')
        return ('\n').join(xml_strings)

    def __cmp__(self, other_database_link):
        if self.compare(other_database_link):
            return 1
        else:
            return 0

    def compare(self, other_db_link):
        """
        Calculate the differences between this db link and <other_db_link>

        @param other_db_link: Another database link to compare to this one
        @type other_db_link: A DatabaseLink object
        @return: The differences between the two database links or nothing if 
          they are equal
        @rtype: String
        """
        response = []
        if self.name != other_db_link.name:
            response.append('DIFF: Database link names: ')
            response.append('%s and %s' % (self.name, other_db_link.name))
        if hasattr(self, 'connection_string') or hasattr(other_db_link, 'connection_string'):
            if hasattr(self, 'connection_string') and hasattr(other_db_link, 'connection_string'):
                if self.connection_string != other_db_link.connection_string:
                    response.append('DIFF: Database link ')
                    response.append('connection strings: ')
                    response.append('%s and ' % self.connection_string)
                    response.append('%s' % other_db_link.connection_string)
            elif not hasattr(self, 'connection_string'):
                response.append('DIFF: Database link %s' % self.name)
                response.append('connection string')
            elif not hasattr(other_db_link, 'connection_string'):
                response.append('DIFF: Database link')
                response.append('%s connection string' % other_db_link.name)
        if len(response) > 0:
            return response


if __name__ == '__main__':
    print 'This module should not be invoked from the command line'
    sys.exit(1)