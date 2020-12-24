# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/db/backends/sqlite3/creation.py
# Compiled at: 2018-07-11 18:15:30
import os, sys
from django.db.backends.creation import BaseDatabaseCreation
from django.utils.six.moves import input

class DatabaseCreation(BaseDatabaseCreation):
    data_types = {'AutoField': 'integer', 
       'BooleanField': 'bool', 
       'CharField': 'varchar(%(max_length)s)', 
       'CommaSeparatedIntegerField': 'varchar(%(max_length)s)', 
       'DateField': 'date', 
       'DateTimeField': 'datetime', 
       'DecimalField': 'decimal', 
       'FileField': 'varchar(%(max_length)s)', 
       'FilePathField': 'varchar(%(max_length)s)', 
       'FloatField': 'real', 
       'IntegerField': 'integer', 
       'BigIntegerField': 'bigint', 
       'IPAddressField': 'char(15)', 
       'GenericIPAddressField': 'char(39)', 
       'NullBooleanField': 'bool', 
       'OneToOneField': 'integer', 
       'PositiveIntegerField': 'integer unsigned', 
       'PositiveSmallIntegerField': 'smallint unsigned', 
       'SlugField': 'varchar(%(max_length)s)', 
       'SmallIntegerField': 'smallint', 
       'TextField': 'text', 
       'TimeField': 'time'}

    def sql_for_pending_references(self, model, style, pending_references):
        """SQLite3 doesn't support constraints"""
        return []

    def sql_remove_table_constraints(self, model, references_to_delete, style):
        """SQLite3 doesn't support constraints"""
        return []

    def _get_test_db_name(self):
        test_database_name = self.connection.settings_dict['TEST_NAME']
        if test_database_name and test_database_name != ':memory:':
            return test_database_name
        return ':memory:'

    def _create_test_db(self, verbosity, autoclobber):
        test_database_name = self._get_test_db_name()
        if test_database_name != ':memory:':
            if verbosity >= 1:
                print "Destroying old test database '%s'..." % self.connection.alias
            if os.access(test_database_name, os.F_OK):
                if not autoclobber:
                    confirm = input("Type 'yes' if you would like to try deleting the test database '%s', or 'no' to cancel: " % test_database_name)
                if autoclobber or confirm == 'yes':
                    try:
                        os.remove(test_database_name)
                    except Exception as e:
                        sys.stderr.write('Got an error deleting the old test database: %s\n' % e)
                        sys.exit(2)

                else:
                    print 'Tests cancelled.'
                    sys.exit(1)
        return test_database_name

    def _destroy_test_db(self, test_database_name, verbosity):
        if test_database_name and test_database_name != ':memory:':
            os.remove(test_database_name)

    def set_autocommit(self):
        self.connection.connection.isolation_level = None
        return

    def test_db_signature(self):
        """
        Returns a tuple that uniquely identifies a test database.

        This takes into account the special cases of ":memory:" and "" for
        SQLite since the databases will be distinct despite having the same
        TEST_NAME. See http://www.sqlite.org/inmemorydb.html
        """
        settings_dict = self.connection.settings_dict
        test_dbname = self._get_test_db_name()
        sig = [self.connection.settings_dict['NAME']]
        if test_dbname == ':memory:':
            sig.append(self.connection.alias)
        return tuple(sig)