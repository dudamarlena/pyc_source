# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/smosker/zero-downtime-migrations/tests/test_create_index.py
# Compiled at: 2018-01-15 08:11:03
# Size of source mod 2**32: 1617 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, re
from django.db import models
from django.db import connections
from django.test.utils import CaptureQueriesContext
from zero_downtime_migrations.backend.schema import DatabaseSchemaEditor
from test_app.models import TestModel
connection = connections['default']
schema_editor = DatabaseSchemaEditor

@pytest.mark.django_db(transaction=True)
def test_create_index_success():
    old_field = models.IntegerField()
    old_field.set_attributes_from_name('name')
    field = models.IntegerField(db_index=True)
    field.set_attributes_from_name('name')
    pattern = 'CREATE INDEX CONCURRENTLY "test_app_testmodel_name_\\w+(_uniq)?" ON "test_app_testmodel" \\("name"\\)'
    with CaptureQueriesContext(connection) as (ctx):
        with schema_editor(connection=connection) as (editor):
            editor.alter_field(TestModel, old_field, field)
            @py_assert2 = ctx.captured_queries
            @py_assert4 = len(@py_assert2)
            @py_assert7 = 1
            @py_assert6 = @py_assert4 == @py_assert7
            if not @py_assert6:
                @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.captured_queries\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(ctx) if 'ctx' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ctx) else 'ctx',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
                @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
                raise AssertionError(@pytest_ar._format_explanation(@py_format11))
            @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
            @py_assert1 = re.search
            @py_assert4 = ctx.captured_queries[0]['sql']
            @py_assert6 = @py_assert1(pattern, @py_assert4)
            @py_assert9 = None
            @py_assert8 = @py_assert6 is not @py_assert9
            if not @py_assert8:
                @py_format11 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py3)s, %(py5)s)\n} is not %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(pattern) if 'pattern' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pattern) else 'pattern',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
                @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
                raise AssertionError(@pytest_ar._format_explanation(@py_format13))
            @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None


def test_sqlmigrate_create_index_working():
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
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.collected_sql\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(editor) if 'editor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(editor) else 'editor',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert1 = re.search
        @py_assert4 = editor.collected_sql[0]
        @py_assert6 = @py_assert1(pattern, @py_assert4)
        @py_assert9 = None
        @py_assert8 = @py_assert6 is not @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.search\n}(%(py3)s, %(py5)s)\n} is not %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(re) if 're' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re) else 're',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(pattern) if 'pattern' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pattern) else 'pattern',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None