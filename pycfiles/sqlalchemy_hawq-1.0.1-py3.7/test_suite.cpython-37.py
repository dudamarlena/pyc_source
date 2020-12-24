# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_suite.py
# Compiled at: 2019-10-07 13:43:57
# Size of source mod 2**32: 1952 bytes
"""
Stub for sqlalchemy's unit tests.
Imports and modifies some test subsuites.

Disables tests of sqlalchemy functionality that Hawq dialect does not support.
"""
from sqlalchemy.testing.suite import *
import sqlalchemy.testing.suite as _SimpleUpdateDeleteTest
import sqlalchemy.testing.suite as _TableDDLTest
import sqlalchemy.testing.suite as _ServerSideCursorsTest

class ComponentReflectionTest:
    __doc__ = '\n    Every test in the ComponentReflectionTest suite relies on indexing.\n    Hawq does not support indexes, so skip all tests.\n\n    TODO: Check if they can be rewritten to run without indexes.\n    '


class SimpleUpdateDeleteTest(_SimpleUpdateDeleteTest):

    @testing.requires.delete_row_statement_for_append_only_table
    def test_delete(self):
        _SimpleUpdateDeleteTest.test_delete(self)

    @testing.requires.update_append_only_statement
    def test_update(self):
        _SimpleUpdateDeleteTest.test_update(self)


class TableDDLTest(_TableDDLTest):

    @testing.requires.test_schema_exists
    def test_create_table_schema(self):
        _TableDDLTest.test_create_table_schema(self)


class ServerSideCursorsTest(_ServerSideCursorsTest):

    def tearDown(self):
        """
        Overrides parent teardown method to prevent calling dispose
        on engine that does not exist if test is skipped.
        """
        engines.testing_reaper.close_all()
        if 'engine' in dir(self):
            self.engine.dispose()

    @testing.requires.update_append_only_statement
    def test_roundtrip(self):
        _ServerSideCursorsTest.test_roundtrip(self)

    @testing.requires.select_for_update_share
    def test_for_update_string(self):
        _ServerSideCursorsTest.test_for_update_string(self)

    @testing.requires.select_for_update_share
    def test_for_update_expr(self):
        _ServerSideCursorsTest.test_for_update_expr(self)