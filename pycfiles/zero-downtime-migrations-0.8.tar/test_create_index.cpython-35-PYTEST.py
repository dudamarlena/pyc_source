# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/smosker/zero-downtime-migrations/tests/test_create_index.py
# Compiled at: 2019-07-03 06:38:34
# Size of source mod 2**32: 3904 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, psycopg2, re, django
from django.db import models
from django.db import connections
from django.test.utils import CaptureQueriesContext
from distutils.version import StrictVersion
from zero_downtime_migrations.backend.schema import DatabaseSchemaEditor
from zero_downtime_migrations.backend.exceptions import InvalidIndexError
from test_app.models import TestModel
connection = connections['default']
schema_editor = DatabaseSchemaEditor
DJANGO_VERISON = StrictVersion(django.get_version())

@pytest.mark.django_db(transaction=True)
def test_create_index_success():
    TestModel.objects.all().delete()
    old_field = models.IntegerField()
    old_field.set_attributes_from_name('name')
    field = models.IntegerField(db_index=True)
    field.set_attributes_from_name('name')
    pattern = 'CREATE INDEX CONCURRENTLY "test_app_testmodel_name_\\w+(_uniq)?" ON "test_app_testmodel" \\("name"\\)'
    search_pattern = "SELECT 1 FROM pg_class, pg_index WHERE pg_index.indisvalid = false AND pg_index.indexrelid = pg_class.oid and pg_class.relname = 'test_app_testmodel_name_\\w+(_uniq)?'"
    with CaptureQueriesContext(connection) as (ctx):
        with schema_editor(connection=connection) as (editor):
            editor.alter_field(TestModel, old_field, field)
            @py_assert2 = ctx.captured_queries
            @py_assert4 = len(@py_assert2)
            @py_assert7 = 2
            @py_assert6 = @py_assert4 == @py_assert7
            if not @py_assert6:
                @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.captured_queries\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1': @pytest_ar._saferepr(ctx) if 'ctx' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ctx) else 'ctx', 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py8': @pytest_ar._saferepr(@py_assert7)}
                @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
                raise AssertionError(@pytest_ar._format_explanation(@py_format11))
            @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
            @py_assert1 = re.search
            @py_assert4 = ctx.captured_queries[0]['sql']
            @py_assert6 = @py_assert1(pattern, @py_assert4)
            @py_assert9 = None
            @py_assert8 = @py_assert6 is not @py_assert9
            if not @py_assert8:
                @py_format11 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py3)s, %(py5)s)\n} is not %(py10)s', ), (@py_assert6, @py_assert9)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(pattern) if 'pattern' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pattern) else 'pattern'}
                @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
            @py_assert1 = re.search
            @py_assert4 = ctx.captured_queries[1]['sql']
            @py_assert6 = @py_assert1(search_pattern, @py_assert4)
            @py_assert9 = None
            @py_assert8 = @py_assert6 is not @py_assert9
            if not @py_assert8:
                @py_format11 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py3)s, %(py5)s)\n} is not %(py10)s', ), (@py_assert6, @py_assert9)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(search_pattern) if 'search_pattern' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(search_pattern) else 'search_pattern'}
                @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


@pytest.mark.django_db(transaction=True)
def test_sqlmigrate_create_index_working():
    TestModel.objects.all().delete()
    old_field = models.IntegerField()
    old_field.set_attributes_from_name('name')
    field = models.IntegerField(db_index=True)
    field.set_attributes_from_name('name')
    pattern = 'CREATE INDEX CONCURRENTLY "test_app_testmodel_name_\\w+(_uniq)?" ON "test_app_testmodel" \\("name"\\)'
    with schema_editor(connection=connection, collect_sql=True) as (editor):
        editor.alter_field(TestModel, old_field, field)
        @py_assert2 = editor.collected_sql
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.collected_sql\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1': @pytest_ar._saferepr(editor) if 'editor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(editor) else 'editor', 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py8': @pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert1 = re.search
        @py_assert4 = editor.collected_sql[0]
        @py_assert6 = @py_assert1(pattern, @py_assert4)
        @py_assert9 = None
        @py_assert8 = @py_assert6 is not @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py3)s, %(py5)s)\n} is not %(py10)s', ), (@py_assert6, @py_assert9)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(pattern) if 'pattern' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pattern) else 'pattern'}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


@pytest.mark.django_db(transaction=True)
def test_create_index_fail():
    TestModel.objects.create(name='test_unique')
    TestModel.objects.create(name='test_unique')
    old_field = models.IntegerField()
    old_field.set_attributes_from_name('name')
    field = models.IntegerField(unique=True)
    field.set_attributes_from_name('name')
    if DJANGO_VERISON > StrictVersion('2.1'):
        create_pattern = 'CREATE UNIQUE INDEX CONCURRENTLY "test_app_testmodel_name_\\w+(_uniq)?" ON "test_app_testmodel" \\("name"\\)'
        search_pattern = "SELECT 1 FROM pg_class, pg_index WHERE pg_index.indisvalid = false AND pg_index.indexrelid = pg_class.oid and pg_class.relname = 'test_app_testmodel_name_\\w+(_uniq)?'"
        drop_pattern = 'DROP INDEX CONCURRENTLY IF EXISTS test_app_testmodel_name_\\w+(_uniq)?'
        with CaptureQueriesContext(connection) as (ctx):
            with schema_editor(connection=connection) as (editor):
                with pytest.raises(InvalidIndexError):
                    editor.alter_field(TestModel, old_field, field)
                @py_assert2 = ctx.captured_queries
                @py_assert4 = len(@py_assert2)
                @py_assert7 = 3
                @py_assert6 = @py_assert4 == @py_assert7
                if not @py_assert6:
                    @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.captured_queries\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1': @pytest_ar._saferepr(ctx) if 'ctx' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ctx) else 'ctx', 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py8': @pytest_ar._saferepr(@py_assert7)}
                    @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format11))
                @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
                @py_assert1 = re.search
                @py_assert4 = ctx.captured_queries[0]['sql']
                @py_assert6 = @py_assert1(create_pattern, @py_assert4)
                @py_assert9 = None
                @py_assert8 = @py_assert6 is not @py_assert9
                if not @py_assert8:
                    @py_format11 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py3)s, %(py5)s)\n} is not %(py10)s', ), (@py_assert6, @py_assert9)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(create_pattern) if 'create_pattern' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(create_pattern) else 'create_pattern'}
                    @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format13))
                @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
                @py_assert1 = re.search
                @py_assert4 = ctx.captured_queries[1]['sql']
                @py_assert6 = @py_assert1(search_pattern, @py_assert4)
                @py_assert9 = None
                @py_assert8 = @py_assert6 is not @py_assert9
                if not @py_assert8:
                    @py_format11 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py3)s, %(py5)s)\n} is not %(py10)s', ), (@py_assert6, @py_assert9)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(search_pattern) if 'search_pattern' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(search_pattern) else 'search_pattern'}
                    @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format13))
                @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
                @py_assert1 = re.search
                @py_assert4 = ctx.captured_queries[2]['sql']
                @py_assert6 = @py_assert1(drop_pattern, @py_assert4)
                @py_assert9 = None
                @py_assert8 = @py_assert6 is not @py_assert9
                if not @py_assert8:
                    @py_format11 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py3)s, %(py5)s)\n} is not %(py10)s', ), (@py_assert6, @py_assert9)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(drop_pattern) if 'drop_pattern' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(drop_pattern) else 'drop_pattern'}
                    @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format13))
                @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    else:
        with CaptureQueriesContext(connection) as (ctx):
            with schema_editor(connection=connection) as (editor):
                with pytest.raises(psycopg2.IntegrityError):
                    editor.alter_field(TestModel, old_field, field)
                @py_assert2 = ctx.captured_queries
                @py_assert4 = len(@py_assert2)
                @py_assert7 = 1
                @py_assert6 = @py_assert4 == @py_assert7
                if not @py_assert6:
                    @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.captured_queries\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1': @pytest_ar._saferepr(ctx) if 'ctx' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ctx) else 'ctx', 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(@py_assert2), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py8': @pytest_ar._saferepr(@py_assert7)}
                    @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format11))
                @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
                print(ctx.captured_queries)
        @py_assert0 = 1
        @py_assert3 = 2
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None