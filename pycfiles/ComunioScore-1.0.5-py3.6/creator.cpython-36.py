# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/db/creator.py
# Compiled at: 2020-04-13 07:58:16
# Size of source mod 2**32: 8227 bytes
import logging
from ComunioScore.db import DBConnector
from ComunioScore.exceptions import DBCreatorError

class Database:
    __doc__ = ' class Database to build a sql string for Database creation\n\n    USAGE:\n            Database(name="web")\n\n    '

    def __init__(self, name):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class Database')
        self.name = name

    def __str__(self):
        """ string representation of database creation

        :return: sql string for database creation
        """
        return 'create database {}'.format(self.name)

    def __repr__(self):
        """ string representation of database object

        :return: sql string for database creation
        """
        return 'create database {}'.format(self.name)


class Schema:
    __doc__ = ' class Schema to build a sql string for Schema creation\n\n    USAGE:\n            Schema(name="credstuffer")\n\n    '

    def __init__(self, name):
        self.logger = logging.getLogger('ComunioScore')
        self.name = name
        self.sql_schema = 'create schema if not exists {}'.format(self.name)

    def __str__(self):
        """ string representation of schema creation

        :return: sql string for schema creation
        """
        return self.sql_schema

    def __repr__(self):
        """ string representation of schema object

        :return: sql string for schema creation
        """
        return self.sql_schema


class Table:
    __doc__ = ' class Table to build a sql string for Table creation\n\n    USAGE:\n            Table("page", Column(\'id\', \'int\', False, False), schema="web")\n            Table("page")\n\n    '

    def __init__(self, name, *columns, schema=None):
        self.logger = logging.getLogger('ComunioScore')
        self.name = name
        self.schema = schema
        self.sql_table = ''
        if schema is None:
            self.sql_table = 'create table if not exists {} '.format(self.name)
        else:
            self.sql_table = 'create table if not exists  {}.{} '.format(self.schema, self.name)
        if len(columns) == 0:
            self.sql_table = self.sql_table + '()'
        else:
            if len(columns) == 1:
                self.sql_table = self.sql_table + str(columns).replace(',', '')
            elif len(columns) > 1:
                self.sql_table = self.sql_table + str(columns)

    def __call__(self, *columns):
        """ implicit method to invoke table instances to create new sql strings with variable *columns objects

        :param columns: objects of type Column()
        :return: sql table creation string
        """
        if len(columns) == 1:
            self.sql_table = self.sql_table + str(columns).replace(',', '')
            return self.sql_table
        if len(columns) > 1:
            self.sql_table = self.sql_table + str(columns)
            return self.sql_table

    def __str__(self):
        """ string representation of table creation

        :return: sql string for table creation
        """
        return self.sql_table

    def __repr__(self):
        """ string representation of table object

        :return: sql string for table creation
        """
        return self.sql_table


class Column:
    __doc__ = " class Column to build a sql string for Column creation\n\n    USAGE:\n            Column(name='id', type='int', not_null=False, prim_key=True)\n\n    "

    def __init__(self, name, type, not_null=False, prim_key=False, exist_table=False, table_name=None, schema=None):
        self.logger = logging.getLogger('ComunioScore')
        self.name = name
        self.type = type
        self.not_null = not_null
        self.prim_key = prim_key
        self.exist_table = exist_table
        self.table_name = table_name
        self.schema = schema
        if self.schema is None:
            self.alter_table = 'alter table {} '.format(self.table_name)
        else:
            self.alter_table = 'alter table {}.{} '.format(self.schema, self.table_name)
        self.name_type_str = '{} {} '.format(self.name, self.type)
        self.add_column_str = 'add column '
        self.primary_key_str = 'primary key '
        self.not_null_str = 'not null '
        self.if_not_exists = 'if not exists '
        self.sql_primary_key = self.name_type_str + self.primary_key_str
        self.sql_not_null = self.name_type_str + self.not_null_str
        self.sql_exist_table = self.alter_table + self.add_column_str + self.if_not_exists + self.name_type_str
        self.sql_exist_table_prim_key = self.sql_exist_table + self.primary_key_str
        self.sql_exit_table_not_null = self.sql_exist_table + self.not_null_str

    def __str__(self):
        """ string representation of column creation

        :return: sql string for column creation
        """
        if self.prim_key:
            if not self.not_null:
                if not self.exist_table:
                    return self.sql_primary_key
                if self.not_null:
                    if not self.prim_key:
                        if not self.exist_table:
                            return self.sql_not_null
            else:
                if self.exist_table:
                    if not self.prim_key:
                        if not self.not_null:
                            return self.sql_exist_table
                if self.exist_table:
                    if self.prim_key:
                        return self.sql_exist_table_prim_key
        else:
            if self.exist_table:
                if self.not_null:
                    return self.sql_exit_table_not_null
        return '{} {} '.format(self.name, self.type)

    def __repr__(self):
        """ string representation of column object

        :return: sql string for column creation
        """
        if self.prim_key:
            if not self.not_null:
                if not self.exist_table:
                    return self.sql_primary_key
                if self.not_null:
                    if not self.prim_key:
                        if not self.exist_table:
                            return self.sql_not_null
            else:
                if self.exist_table:
                    if not self.prim_key:
                        if not self.not_null:
                            return self.sql_exist_table
                if self.exist_table:
                    if self.prim_key:
                        return self.sql_exist_table_prim_key
        else:
            if self.exist_table:
                if self.not_null:
                    return self.sql_exit_table_not_null
        return '{} {} '.format(self.name, self.type)


class DBCreator(DBConnector):
    __doc__ = ' class DBCreator to build database, table or column\n\n    USAGE:\n            creator = DBCreator()\n            creator.connect(host, port, username, password, dbname, minConn=1, maxConn=10)\n            creator.build(obj=Database(name="web"))\n            creator.build(obj=Table("gps", Column(\'did\', \'text\'), Column(\'ts\', \'text\')))\n\n    '

    def __init__(self):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class DBCreator')
        super().__init__()

    def build(self, obj):
        """ build object depending on given object 'obj'

        """
        if isinstance(obj, Database):
            self._DBCreator__database(obj)
        else:
            if isinstance(obj, Schema):
                self._DBCreator__schema(obj)
            else:
                if isinstance(obj, Table):
                    self._DBCreator__table(obj)
                else:
                    if isinstance(obj, Column):
                        self._DBCreator__column(obj)
                    else:
                        raise DBCreatorError('Provide either a Database, Schema, Table or Column object')

    def __database(self, database_obj):
        """ creates a database

        :param database_obj: database object
        """
        with self.get_cursor(autocommit=True) as (cursor):
            cursor.execute(str(database_obj))

    def __schema(self, schema_obj):
        """creates a Schema

        :param schema_obj: schema object
        """
        with self.get_cursor() as (cursor):
            cursor.execute(str(schema_obj))

    def __table(self, table_obj):
        """ creates a table

        :param table_obj: table object
        """
        with self.get_cursor() as (cursor):
            cursor.execute(str(table_obj))

    def __column(self, column_obj):
        """ creates a column

        :param column_obj: column object
        """
        if column_obj.exist_table:
            with self.get_cursor() as (cursor):
                cursor.execute(str(column_obj))
        else:
            raise DBCreatorError('Creation of column object is only possible in existing tables')