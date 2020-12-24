# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/smosker/zero-downtime-migrations/tests/test_add_field.py
# Compiled at: 2018-01-10 05:49:33
# Size of source mod 2**32: 16884 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, pytz
from datetime import datetime
from django.db import models
from django.db import connections
from django.test.utils import CaptureQueriesContext
from freezegun import freeze_time
from zero_downtime_migrations.backend.schema import DatabaseSchemaEditor
from test_app.models import TestModel
pytestmark = pytest.mark.django_db
connection = connections['default']
schema_editor = DatabaseSchemaEditor

def column_classes(model):
    with connection.cursor() as (cursor):
        columns = {d[0]:(connection.introspection.get_field_type(d[1], d), d) for d in connection.introspection.get_table_description(cursor, model._meta.db_table)}
    return columns


def test_sqlmigrate_add_field_working():
    field = models.BooleanField(default=True)
    field.set_attributes_from_name('bool_field')
    with CaptureQueriesContext(connection) as (ctx):
        with schema_editor(connection=connection, collect_sql=True) as (editor):
            editor.add_field(TestModel, field)
            @py_assert1 = editor.collected_sql
            @py_assert4 = [
             "SELECT IS_NULLABLE, DATA_TYPE, COLUMN_DEFAULT from information_schema.columns where table_name = 'test_app_testmodel' and column_name = 'bool_field';", 'ALTER TABLE "test_app_testmodel" ADD COLUMN "bool_field" boolean NULL;', 'ALTER TABLE "test_app_testmodel" ALTER COLUMN "bool_field" SET DEFAULT true;', "SELECT reltuples::BIGINT FROM pg_class WHERE relname = 'test_app_testmodel';", '\n                       WITH cte AS (\n                       SELECT id as pk\n                       FROM test_app_testmodel\n                       WHERE  bool_field is null\n                       LIMIT  1000\n                       )\n                       UPDATE test_app_testmodel table_\n                       SET bool_field = true\n                       FROM   cte\n                       WHERE  table_.id = cte.pk\n                       ;', 'ALTER TABLE "test_app_testmodel" ALTER COLUMN "bool_field" SET NOT NULL;', 'ALTER TABLE "test_app_testmodel" ALTER COLUMN "bool_field" DROP DEFAULT;']
            @py_assert3 = @py_assert1 == @py_assert4
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.collected_sql\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(editor) if 'editor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(editor) else 'editor'}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None


def test_add_bool_field_no_existed_objects_success():
    columns = column_classes(TestModel)
    @py_assert0 = 'bool_field'
    @py_assert2 = @py_assert0 not in columns
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, columns)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(columns) if 'columns' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(columns) else 'columns'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    field = models.BooleanField(default=True)
    field.set_attributes_from_name('bool_field')
    with CaptureQueriesContext(connection) as (ctx):
        with schema_editor(connection=connection) as (editor):
            editor.add_field(TestModel, field)
    columns = column_classes(TestModel)
    @py_assert0 = columns['bool_field'][0]
    @py_assert3 = 'BooleanField'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    queries = [query_data['sql'] for query_data in ctx.captured_queries if 'test_app' in query_data['sql']]
    expected_queries = ["SELECT IS_NULLABLE, DATA_TYPE, COLUMN_DEFAULT from information_schema.columns where table_name = 'test_app_testmodel' and column_name = 'bool_field';",
     'ALTER TABLE "test_app_testmodel" ADD COLUMN "bool_field" boolean NULL',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "bool_field" SET DEFAULT true',
     "SELECT reltuples::BIGINT FROM pg_class WHERE relname = 'test_app_testmodel';",
     'SELECT COUNT(*) FROM test_app_testmodel;',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "bool_field" SET NOT NULL',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "bool_field" DROP DEFAULT']
    @py_assert1 = queries == expected_queries
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (queries, expected_queries)) % {'py2': @pytest_ar._saferepr(expected_queries) if 'expected_queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_queries) else 'expected_queries', 'py0': @pytest_ar._saferepr(queries) if 'queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(queries) else 'queries'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_add_bool_field_with_existed_object_success(test_object):
    columns = column_classes(TestModel)
    @py_assert0 = 'bool_field'
    @py_assert2 = @py_assert0 not in columns
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, columns)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(columns) if 'columns' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(columns) else 'columns'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    field = models.BooleanField(default=True)
    field.set_attributes_from_name('bool_field')
    with CaptureQueriesContext(connection) as (ctx):
        with schema_editor(connection=connection) as (editor):
            editor.add_field(TestModel, field)
            queries = [query_data['sql'] for query_data in ctx.captured_queries if 'test_app' in query_data['sql']]
    columns = column_classes(TestModel)
    @py_assert0 = columns['bool_field'][0]
    @py_assert3 = 'BooleanField'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    expected_queries = ["SELECT IS_NULLABLE, DATA_TYPE, COLUMN_DEFAULT from information_schema.columns where table_name = 'test_app_testmodel' and column_name = 'bool_field';",
     'ALTER TABLE "test_app_testmodel" ADD COLUMN "bool_field" boolean NULL',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "bool_field" SET DEFAULT true',
     "SELECT reltuples::BIGINT FROM pg_class WHERE relname = 'test_app_testmodel';",
     'SELECT COUNT(*) FROM test_app_testmodel;',
     '\n                       WITH cte AS (\n                       SELECT id as pk\n                       FROM test_app_testmodel\n                       WHERE  bool_field is null\n                       LIMIT  1000\n                       )\n                       UPDATE test_app_testmodel table_\n                       SET bool_field = true\n                       FROM   cte\n                       WHERE  table_.id = cte.pk\n                       ',
     '\n                       WITH cte AS (\n                       SELECT id as pk\n                       FROM test_app_testmodel\n                       WHERE  bool_field is null\n                       LIMIT  1000\n                       )\n                       UPDATE test_app_testmodel table_\n                       SET bool_field = true\n                       FROM   cte\n                       WHERE  table_.id = cte.pk\n                       ',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "bool_field" SET NOT NULL',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "bool_field" DROP DEFAULT']
    @py_assert1 = queries == expected_queries
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (queries, expected_queries)) % {'py2': @pytest_ar._saferepr(expected_queries) if 'expected_queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_queries) else 'expected_queries', 'py0': @pytest_ar._saferepr(queries) if 'queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(queries) else 'queries'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    sql = 'SELECT * from "test_app_testmodel" where id = %s'
    with connection.cursor() as (cursor):
        cursor.execute(sql, (test_object.id,))
        result = cursor.fetchall()
    @py_assert2 = [
     (
      test_object.id, test_object.name, True)]
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_add_bool_field_with_existed_many_objects_success(test_object, test_object_two, test_object_three):
    columns = column_classes(TestModel)
    @py_assert0 = 'bool_field'
    @py_assert2 = @py_assert0 not in columns
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, columns)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(columns) if 'columns' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(columns) else 'columns'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    field = models.BooleanField(default=True)
    field.set_attributes_from_name('bool_field')
    with CaptureQueriesContext(connection) as (ctx):
        with schema_editor(connection=connection) as (editor):
            editor.add_field(TestModel, field)
            queries = [query_data['sql'] for query_data in ctx.captured_queries if 'test_app' in query_data['sql']]
    columns = column_classes(TestModel)
    @py_assert0 = columns['bool_field'][0]
    @py_assert3 = 'BooleanField'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    expected_queries = ["SELECT IS_NULLABLE, DATA_TYPE, COLUMN_DEFAULT from information_schema.columns where table_name = 'test_app_testmodel' and column_name = 'bool_field';",
     'ALTER TABLE "test_app_testmodel" ADD COLUMN "bool_field" boolean NULL',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "bool_field" SET DEFAULT true',
     "SELECT reltuples::BIGINT FROM pg_class WHERE relname = 'test_app_testmodel';",
     'SELECT COUNT(*) FROM test_app_testmodel;',
     '\n                       WITH cte AS (\n                       SELECT id as pk\n                       FROM test_app_testmodel\n                       WHERE  bool_field is null\n                       LIMIT  1000\n                       )\n                       UPDATE test_app_testmodel table_\n                       SET bool_field = true\n                       FROM   cte\n                       WHERE  table_.id = cte.pk\n                       ',
     '\n                       WITH cte AS (\n                       SELECT id as pk\n                       FROM test_app_testmodel\n                       WHERE  bool_field is null\n                       LIMIT  1000\n                       )\n                       UPDATE test_app_testmodel table_\n                       SET bool_field = true\n                       FROM   cte\n                       WHERE  table_.id = cte.pk\n                       ',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "bool_field" SET NOT NULL',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "bool_field" DROP DEFAULT']
    @py_assert1 = queries == expected_queries
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (queries, expected_queries)) % {'py2': @pytest_ar._saferepr(expected_queries) if 'expected_queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_queries) else 'expected_queries', 'py0': @pytest_ar._saferepr(queries) if 'queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(queries) else 'queries'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    sql = 'SELECT * from "test_app_testmodel" where id = ANY(%s) ORDER BY id'
    with connection.cursor() as (cursor):
        cursor.execute(sql, ([test_object.id, test_object_two.id, test_object_three.id],))
        result = cursor.fetchall()
    @py_assert2 = [
     (
      test_object.id, test_object.name, True), (test_object_two.id, test_object_two.name, True), (test_object_three.id, test_object_three.name, True)]
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@freeze_time('2017-12-15 03:21:34', tz_offset=-3)
def test_add_datetime_field_no_existed_objects_success():
    columns = column_classes(TestModel)
    @py_assert0 = 'datetime_field'
    @py_assert2 = @py_assert0 not in columns
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, columns)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(columns) if 'columns' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(columns) else 'columns'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    field = models.DateTimeField(default=datetime.now)
    field.set_attributes_from_name('datetime_field')
    with CaptureQueriesContext(connection) as (ctx):
        with schema_editor(connection=connection) as (editor):
            editor.add_field(TestModel, field)
            queries = [query_data['sql'] for query_data in ctx.captured_queries if 'test_app' in query_data['sql']]
    columns = column_classes(TestModel)
    @py_assert0 = columns['datetime_field'][0]
    @py_assert3 = 'DateTimeField'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    expected_queries = ["SELECT IS_NULLABLE, DATA_TYPE, COLUMN_DEFAULT from information_schema.columns where table_name = 'test_app_testmodel' and column_name = 'datetime_field';",
     'ALTER TABLE "test_app_testmodel" ADD COLUMN "datetime_field" timestamp with time zone NULL',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "datetime_field" SET DEFAULT \'2017-12-15T00:21:34+00:00\'::timestamptz',
     "SELECT reltuples::BIGINT FROM pg_class WHERE relname = 'test_app_testmodel';",
     'SELECT COUNT(*) FROM test_app_testmodel;',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "datetime_field" SET NOT NULL',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "datetime_field" DROP DEFAULT']
    @py_assert1 = queries == expected_queries
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (queries, expected_queries)) % {'py2': @pytest_ar._saferepr(expected_queries) if 'expected_queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_queries) else 'expected_queries', 'py0': @pytest_ar._saferepr(queries) if 'queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(queries) else 'queries'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


@freeze_time('2017-12-15 03:21:34', tz_offset=-3)
def test_add_datetime_field_with_existed_object_success(test_object):
    columns = column_classes(TestModel)
    @py_assert0 = 'datetime_field'
    @py_assert2 = @py_assert0 not in columns
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, columns)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(columns) if 'columns' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(columns) else 'columns'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    field = models.DateTimeField(default=datetime.now)
    field.set_attributes_from_name('datetime_field')
    with CaptureQueriesContext(connection) as (ctx):
        with schema_editor(connection=connection) as (editor):
            editor.add_field(TestModel, field)
            queries = [query_data['sql'] for query_data in ctx.captured_queries if 'test_app' in query_data['sql']]
    columns = column_classes(TestModel)
    @py_assert0 = columns['datetime_field'][0]
    @py_assert3 = 'DateTimeField'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    expected_queries = ["SELECT IS_NULLABLE, DATA_TYPE, COLUMN_DEFAULT from information_schema.columns where table_name = 'test_app_testmodel' and column_name = 'datetime_field';",
     'ALTER TABLE "test_app_testmodel" ADD COLUMN "datetime_field" timestamp with time zone NULL',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "datetime_field" SET DEFAULT \'2017-12-15T00:21:34+00:00\'::timestamptz',
     "SELECT reltuples::BIGINT FROM pg_class WHERE relname = 'test_app_testmodel';",
     'SELECT COUNT(*) FROM test_app_testmodel;',
     "\n                       WITH cte AS (\n                       SELECT id as pk\n                       FROM test_app_testmodel\n                       WHERE  datetime_field is null\n                       LIMIT  1000\n                       )\n                       UPDATE test_app_testmodel table_\n                       SET datetime_field = '2017-12-15T00:21:34+00:00'::timestamptz\n                       FROM   cte\n                       WHERE  table_.id = cte.pk\n                       ",
     "\n                       WITH cte AS (\n                       SELECT id as pk\n                       FROM test_app_testmodel\n                       WHERE  datetime_field is null\n                       LIMIT  1000\n                       )\n                       UPDATE test_app_testmodel table_\n                       SET datetime_field = '2017-12-15T00:21:34+00:00'::timestamptz\n                       FROM   cte\n                       WHERE  table_.id = cte.pk\n                       ",
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "datetime_field" SET NOT NULL',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "datetime_field" DROP DEFAULT']
    @py_assert1 = queries == expected_queries
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (queries, expected_queries)) % {'py2': @pytest_ar._saferepr(expected_queries) if 'expected_queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_queries) else 'expected_queries', 'py0': @pytest_ar._saferepr(queries) if 'queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(queries) else 'queries'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    sql = 'SELECT * from "test_app_testmodel" where id = %s'
    with connection.cursor() as (cursor):
        cursor.execute(sql, (test_object.id,))
        result = cursor.fetchall()
    @py_assert2 = [
     (
      test_object.id, test_object.name, datetime(2017, 12, 15, 0, 21, 34, tzinfo=pytz.UTC))]
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


@freeze_time('2017-12-15 03:21:34', tz_offset=-3)
def test_add_datetime_field_with_existed_many_objects_success(test_object, test_object_two, test_object_three):
    columns = column_classes(TestModel)
    @py_assert0 = 'datetime_field'
    @py_assert2 = @py_assert0 not in columns
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, columns)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(columns) if 'columns' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(columns) else 'columns'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    field = models.DateTimeField(default=datetime.now)
    field.set_attributes_from_name('datetime_field')
    with CaptureQueriesContext(connection) as (ctx):
        with schema_editor(connection=connection) as (editor):
            editor.add_field(TestModel, field)
            queries = [query_data['sql'] for query_data in ctx.captured_queries if 'test_app' in query_data['sql']]
    columns = column_classes(TestModel)
    @py_assert0 = columns['datetime_field'][0]
    @py_assert3 = 'DateTimeField'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    expected_queries = ["SELECT IS_NULLABLE, DATA_TYPE, COLUMN_DEFAULT from information_schema.columns where table_name = 'test_app_testmodel' and column_name = 'datetime_field';",
     'ALTER TABLE "test_app_testmodel" ADD COLUMN "datetime_field" timestamp with time zone NULL',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "datetime_field" SET DEFAULT \'2017-12-15T00:21:34+00:00\'::timestamptz',
     "SELECT reltuples::BIGINT FROM pg_class WHERE relname = 'test_app_testmodel';",
     'SELECT COUNT(*) FROM test_app_testmodel;',
     "\n                       WITH cte AS (\n                       SELECT id as pk\n                       FROM test_app_testmodel\n                       WHERE  datetime_field is null\n                       LIMIT  1000\n                       )\n                       UPDATE test_app_testmodel table_\n                       SET datetime_field = '2017-12-15T00:21:34+00:00'::timestamptz\n                       FROM   cte\n                       WHERE  table_.id = cte.pk\n                       ",
     "\n                       WITH cte AS (\n                       SELECT id as pk\n                       FROM test_app_testmodel\n                       WHERE  datetime_field is null\n                       LIMIT  1000\n                       )\n                       UPDATE test_app_testmodel table_\n                       SET datetime_field = '2017-12-15T00:21:34+00:00'::timestamptz\n                       FROM   cte\n                       WHERE  table_.id = cte.pk\n                       ",
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "datetime_field" SET NOT NULL',
     'ALTER TABLE "test_app_testmodel" ALTER COLUMN "datetime_field" DROP DEFAULT']
    @py_assert1 = queries == expected_queries
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (queries, expected_queries)) % {'py2': @pytest_ar._saferepr(expected_queries) if 'expected_queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_queries) else 'expected_queries', 'py0': @pytest_ar._saferepr(queries) if 'queries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(queries) else 'queries'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    sql = 'SELECT * from "test_app_testmodel" where id = ANY(%s) ORDER BY id'
    with connection.cursor() as (cursor):
        cursor.execute(sql, ([test_object.id, test_object_two.id, test_object_three.id],))
        result = cursor.fetchall()
    @py_assert2 = [
     (
      test_object.id, test_object.name, datetime(2017, 12, 15, 0, 21, 34, tzinfo=pytz.UTC)), (test_object_two.id, test_object_two.name, datetime(2017, 12, 15, 0, 21, 34, tzinfo=pytz.UTC)), (test_object_three.id, test_object_three.name, datetime(2017, 12, 15, 0, 21, 34, tzinfo=pytz.UTC))]
    @py_assert1 = result == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (result, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None