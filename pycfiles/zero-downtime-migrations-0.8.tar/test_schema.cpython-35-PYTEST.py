# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/smosker/zero-downtime-migrations/tests/test_schema.py
# Compiled at: 2018-01-17 03:05:22
# Size of source mod 2**32: 2400 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from mock import patch
from django.db import models
from django.db import connections
from django.db.migrations.questioner import InteractiveMigrationQuestioner
from django.test.utils import CaptureQueriesContext
from zero_downtime_migrations.backend.schema import DatabaseSchemaEditor
from test_app.models import TestModel
pytestmark = pytest.mark.django_db
connection = connections['default']
schema_editor = DatabaseSchemaEditor

@pytest.fixture
def add_column():
    sql = 'ALTER TABLE "test_app_testmodel" ADD COLUMN "bool_field" BOOLEAN NULL;'
    with connection.cursor() as (cursor):
        cursor.execute(sql, ())


def test_retry_with_skip_working(add_column):
    field = models.BooleanField(default=True)
    field.set_attributes_from_name('bool_field')
    with CaptureQueriesContext(connection) as (ctx):
        with patch.object(InteractiveMigrationQuestioner, '_choice_input') as (choice_mock):
            with schema_editor(connection=connection) as (editor):
                choice_mock.return_value = 5
                editor.add_field(TestModel, field)
                choice_mock.assert_called_once_with('It look like column "bool_field" in table "test_app_testmodel" already exist with following parameters: TYPE: "boolean", DEFAULT: "None", NULLABLE: "YES".', ('abort migration',
                                                                                                                                                                                                                   'drop column and run migration from beginning',
                                                                                                                                                                                                                   'manually choose action to start from',
                                                                                                                                                                                                                   'show how many rows still need to be updated',
                                                                                                                                                                                                                   'mark operation as successful and proceed to next operation'))
                queries = [query_data['sql'] for query_data in ctx.captured_queries if 'test_app' in query_data['sql']]
                @py_assert2 = len(queries)
                @py_assert5 = 1
                @py_assert4 = @py_assert2 == @py_assert5
                if not @py_assert4:
                    @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(queries) if 'queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(queries) else 'queries', 'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2)}
                    @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format9))
                @py_assert2 = @py_assert4 = @py_assert5 = None
                @py_assert0 = queries[0]
                @py_assert3 = "SELECT IS_NULLABLE, DATA_TYPE, COLUMN_DEFAULT from information_schema.columns where table_name = 'test_app_testmodel' and column_name = 'bool_field';"
                @py_assert2 = @py_assert0 == @py_assert3
                if not @py_assert2:
                    @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
                    @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format7))
                @py_assert0 = @py_assert2 = @py_assert3 = None