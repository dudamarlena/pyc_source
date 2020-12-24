# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gerald/mysql_schema.py
# Compiled at: 2010-10-31 02:23:23
"""
Introduction
============
Capture, document, and manage MySQL database schemas.

This is the mysql_schema module, it contains one useful class, Schema. This 
is a sub-class of Schema (from the schema.py file in this directory).

A schema is comprised of collections of tables, views, stored code objects, 
triggers, and other assorted 'objects'

For reference, here are the current valid data types in MySQL

Text Data Types
---------------

'char', 'varchar', 'tibyblob', 'tinytext', 'blob', 'text', 'mediumblob', 
'mediumtext', 'longblob', 'longtext'

Numeric Data Types
------------------
'int', 'tinyint', 'smallint', 'mediumint', 'bigint', 'float', 'double', 
'decimal'

Meta-data
=========
  Module  : mysql_schema.py
 
  License : BSD License (see LICENSE.txt)

"""
__author__ = 'Andrew J Todd esq <andy47@halfcooked.com>'
__date__ = (2010, 6, 16)
__version__ = (0, 4, 1)
import sys
from gerald.schema import Schema as root_Schema
from gerald.schema import Table as root_Table
from gerald.schema import View as root_View
from gerald.schema import LOG
DATE_DATATYPES = ('date', 'datetime', 'time', 'timestamp', 'year')
COMPLEX_DATATYPES = ('enum', )

class Schema(root_Schema):
    """
    A representation of a MySQL database schema
    
    A MySQL schema is a database on a particular host. This module currently 
    doesn't support triggers although it may do so in a future release. 
    
    MySQL has no sequence objects so there is no implementation to support them 
    in this module.
    """

    def _get_schema(self, cursor):
        """
        Get definitions for the objects in the current schema
        
        @param cursor: The cursor to use to query the data dictionary
        @type cursor: Database cursor object
        @return: All of the objects in this schema
        @rtype: Dictionary
        """
        LOG.info('Getting details for MySQL schema %s from database' % self.name)
        schema = {}
        stmt = "SELECT table_name \n                  FROM   information_schema.tables\n                  WHERE  table_type = 'BASE TABLE'\n               "
        cursor.execute(stmt)
        for table_row in self._cursor.fetchall():
            table = table_row[0]
            LOG.debug('Getting details for table %s' % table)
            schema[table] = Table(table, cursor)

        stmt = "SELECT table_name \n                  FROM   information_schema.tables\n                  WHERE  table_type = 'VIEW'\n               "
        cursor.execute(stmt)
        for view_row in self._cursor.fetchall():
            view = view_row[0]
            LOG.debug('Getting details for view %s' % view)
            schema[view] = View(view, cursor)

        LOG.info('Got details for schema %s' % self.name)
        return schema


class MySqlCalcPrecisionMixin(object):
    """Class to contain the calc_precision static method to be used as a 
    mixin by other classes in this module.
    """

    def calc_precision(data_type, data_length, data_precision=None, data_scale=None):
        """
        Calculate and then retun the precision of a column
        
        The value returned will depend on the provided values, if we just
        receive data_length then we return that encapsulated in braces, if
        we get data_precision and data_scale (for a numeric column for instance)
        we return those encapsulated with braces.

        This is a bit of a hack and should be replaced when columns become
        first class objects.

        @param data_type: The data type of the column
        @type data_type: String
        @param data_length: The length of the column, if this is present it is 
        usually the only numeric value provided
        @type data_length: Integer
        @param data_precision: The total number of digits in the column
        @type data_precision: Integer
        @param data_scale: The number of digits after the decimal point
        @type data_scale: Integer
        @return: The appropriate precision values for this column
        @rtype: String
        """
        if not data_type:
            raise ValueError, 'data_type parameter is mandatory'
        else:
            if data_type in DATE_DATATYPES:
                return ''
            if data_length:
                if data_length > 0:
                    return '(%s)' % data_length
                raise ValueError, 'Data length must be greater than 0'
            else:
                if data_precision > 0 and data_scale >= 0:
                    return '(%s,%s)' % (data_precision, data_scale)
                raise ValueError, 'data_length, data_precision and data_scale must be non-zero for data type %s' % data_type

    calc_precision = staticmethod(calc_precision)


class Table(root_Table, MySqlCalcPrecisionMixin):
    """
    A representation of a database table.
    
    A table is made up of columns and will have indexes, triggers, primary keys 
    and foreign keys.

    Note that MySQL doesn't support tablespaces, but does have a table_type.
    """

    def _get_table(self, cursor):
        """
        Query the data dictionary for the details of this table

        This relies on the read only views within the information_schema 
        database
        
        @param cursor: All of the select statements will be executed using this
          cursor.
        @type cursor: Database cursor object
        """
        stmt = 'SELECT table_schema, engine \n                  FROM   information_schema.tables\n                  WHERE  table_name=%s\n               '
        cursor.execute(stmt, (self.name,))
        LOG.debug('Getting engine for table %s' % self.name)
        result = cursor.fetchone()
        if result is None:
            raise AttributeError, "Can't get DDL for table %s" % self.name
        (self.schema, self.table_type) = result
        stmt = 'SELECT ordinal_position, column_name, data_type,\n                         character_maximum_length, numeric_precision,\n                         numeric_scale, extra, is_nullable, column_key,\n                         column_type\n                  FROM   information_schema.columns\n                  WHERE  table_schema=%s\n                  AND    table_name=%s\n               '
        cursor.execute(stmt, (self.schema, self.name))
        LOG.debug('Getting columns for table %s' % self.name)
        for row in cursor.fetchall():
            column = {'sequence': row[0], 'name': row[1]}
            column['type'] = row[2]
            column['length'] = row[3]
            column['precision'] = row[4]
            column['scale'] = row[5]
            if column['type'] == 'enum':
                column['special'] = row[9].split('(')[1][:-1]
            elif row[6]:
                column['special'] = row[6]
            if row[7] == 'YES':
                column['nullable'] = True
            else:
                column['nullable'] = False
            self.columns[column['name']] = column

        cons_stmt = 'SELECT constraint_name, constraint_type\n                       FROM   information_schema.table_constraints\n                       WHERE  table_schema=%s\n                       AND    table_name=%s\n                    '
        cons_cols_stmt = 'SELECT column_name, referenced_table_name,\n                                   referenced_column_name\n                            FROM   information_schema.key_column_usage\n                            WHERE  table_schema=%s\n                            AND    table_name=%s\n                            AND    constraint_name=%s\n                         '
        cursor.execute(cons_stmt, (self.schema, self.name))
        LOG.debug('Getting constraints for table %s' % self.name)
        for row in cursor.fetchall():
            constraint = {'name': row[0], 'enabled': True}
            if row[1] == 'PRIMARY KEY':
                constraint['type'] = 'Primary'
            elif row[1] == 'FOREIGN KEY':
                constraint['type'] = 'Foreign'
            else:
                constraint['type'] = row[1].capitalize()
            if constraint['type'] in ('Primary', 'Foreign'):
                cursor.execute(cons_cols_stmt, (self.schema, self.name, row[0]))
                constraint_cols = cursor.fetchall()
                constraint['columns'] = [ r[0] for r in constraint_cols ]
            if constraint['type'] == 'Foreign':
                constraint['reftable'] = constraint_cols[0][1]
                constraint['refcolumns'] = [ x[2] for x in constraint_cols ]
                constraint['refpk'] = 'PRIMARY'
            self.constraints[constraint['name']] = constraint

        index_stmt = "SELECT distinct index_name, non_unique, index_type\n                        FROM   information_schema.statistics \n                        WHERE  table_schema=%s\n                        AND    table_name=%s\n                        AND    index_name != 'PRIMARY'"
        ind_col_stmt = 'SELECT column_name\n                          FROM   information_schema.statistics\n                          WHERE  table_schema=%s\n                          AND    table_name=%s\n                          AND    index_name=%s\n                          ORDER BY seq_in_index'
        cursor.execute(index_stmt, (self.schema, self.name))
        LOG.debug('Getting index details for %s' % self.name)
        for index in cursor.fetchall():
            index_dict = {'name': index[0], 'type': index[2]}
            if index[1] == 0:
                index_dict['unique'] = True
            else:
                index_dict['unique'] = False
            cursor.execute(ind_col_stmt, (self.schema, self.name, index[0]))
            index_dict['columns'] = [ x[0] for x in cursor.fetchall() ]
            self.indexes[index_dict['name']] = index_dict

        stmt = 'SHOW CREATE TABLE %s' % self.name
        LOG.debug('Getting DDL for table %s' % self.name)
        cursor.execute(stmt)
        self._sql = cursor.fetchone()[1]
        return

    def get_ddl(self):
        """
        Generate the DDL necessary to create this table in a MySQL database
        
        @return: DDL to create this table
        @rtype: String
        """
        if hasattr(self, '_sql') and len(self.indexes) == 0:
            ddl_strings = self._sql
        else:
            if not hasattr(self, 'name') or self.name == None:
                raise AttributeError, "Can't generate DDL for a table without a name"
            ddl_strings = [
             'CREATE TABLE %s' % self.name]
            in_columns = False
            deco_cols = [ (x['sequence'], x) for x in self.columns.values() ]
            deco_cols.sort()
            sorted_cols = [ col for (seq, col) in deco_cols ]
            for column in sorted_cols:
                if in_columns:
                    ddl_strings.append(', ')
                else:
                    ddl_strings.append(' (')
                    in_columns = True
                ddl_strings.append('%s ' % column['name'])
                ddl_strings.append(column['type'])
                if 'precision' in column:
                    ddl_strings.append(self.calc_precision(column['type'], column['length'], column['precision'], column['scale']))
                elif 'length' in column:
                    ddl_strings.append(self.calc_precision(column['type'], column['length']))
                else:
                    ddl_strings.append(column['type'])
                if not column['nullable']:
                    ddl_strings.append(' NOT NULL')
                if 'default' in column:
                    ddl_strings.append(' DEFAULT ' + column['default'])
                ddl_strings.append(')')

            if 'PRIMARY' in self.constraints:
                ddl_strings.append(', PRIMARY KEY')
                pk_columns = (',').join(self.constraints['PRIMARY']['columns'])
                ddl_strings.append('( %s )' % pk_columns)
            for index in self.indexes:
                ddl_strings.append(', INDEX %s ( ' % index)
                ddl_strings.append('%s )' % self.indexes[index]['columns'])

            if self.table_type:
                ddl_strings.append(' ENGINE=%s' % self.table_type)
        return ('').join(ddl_strings)


class View(root_View, MySqlCalcPrecisionMixin):
    """A representation of a database view
    
    Views were introduced in MySQL 5.1, we need to check which version of the
    database we are running before creating a view
    """

    def __init__(self, view_name, cursor=None, schema=None):
        if cursor:
            cursor.execute('SELECT version()')
            version = cursor.fetchone()[0]
            try:
                release = float(version[:3])
            except ValueError:
                release = 0.1
            else:
                if release < 5.1:
                    raise NotImplementedError, 'Views are not supported in this version of MySQL'
        root_View.__init__(self, view_name, cursor, schema)

    def _get_view(self, cursor):
        """
        Query the data dictionary for this view

        @param cursor: All of the select statements will be executed using this
          cursor.
        @type cursor: Database cursor object
        """
        stmt = 'SELECT view_definition\n                  FROM   information_schema.views\n                  WHERE  table_name = %s'
        cursor.execute(stmt, (self.name,))
        LOG.debug('Getting text for view %s' % self.name)
        self.sql = cursor.fetchone()[0]
        stmt = 'SELECT ordinal_position, column_name, data_type,\n                         character_maximum_length, numeric_precision,\n                         numeric_scale, extra, is_nullable, column_key,\n                         column_type\n                  FROM   information_schema.columns\n                  WHERE  table_name=%s\n               '
        cursor.execute(stmt, (self.name,))
        LOG.debug('Getting columns for index %s' % self.name)
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
            self.columns[col_name] = column

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


if __name__ == '__main__':
    print 'This module should not be invoked from the command line'
    sys.exit(1)