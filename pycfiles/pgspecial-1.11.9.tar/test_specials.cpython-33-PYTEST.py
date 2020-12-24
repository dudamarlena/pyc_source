# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/irina/src/pgspecial/tests/test_specials.py
# Compiled at: 2017-08-13 20:35:56
# Size of source mod 2**32: 14547 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from dbutils import dbtest, POSTGRES_USER
import itertools
objects_listing_headers = [
 'Schema', 'Name', 'Type', 'Owner', 'Size', 'Description']

@dbtest
def test_slash_d(executor):
    results = executor('\\d')
    title = None
    rows = [('public', 'mvw1', 'materialized view', POSTGRES_USER),
     (
      'public', 'tbl1', 'table', POSTGRES_USER),
     (
      'public', 'tbl2', 'table', POSTGRES_USER),
     (
      'public', 'tbl2_id2_seq', 'sequence', POSTGRES_USER),
     (
      'public', 'tbl3', 'table', POSTGRES_USER),
     (
      'public', 'vw1', 'view', POSTGRES_USER)]
    headers = objects_listing_headers[:-2]
    status = 'SELECT 6'
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_d_verbose(executor):
    results = executor('\\d+')
    title = None
    rows = [('public', 'mvw1', 'materialized view', POSTGRES_USER, '8192 bytes', None),
     (
      'public', 'tbl1', 'table', POSTGRES_USER, '8192 bytes', None),
     (
      'public', 'tbl2', 'table', POSTGRES_USER, '8192 bytes', None),
     (
      'public', 'tbl2_id2_seq', 'sequence', POSTGRES_USER, '8192 bytes', None),
     (
      'public', 'tbl3', 'table', POSTGRES_USER, '0 bytes', None),
     (
      'public', 'vw1', 'view', POSTGRES_USER, '0 bytes', None)]
    headers = objects_listing_headers
    status = 'SELECT 6'
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_d_table(executor):
    results = executor('\\d tbl1')
    title = None
    rows = [['id1', 'integer', ' not null'],
     [
      'txt1', 'text', ' not null']]
    headers = [
     'Column', 'Type', 'Modifiers']
    status = 'Indexes:\n    "id_text" PRIMARY KEY, btree (id1, txt1)\n'
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_d_table_verbose(executor):
    results = executor('\\d+ tbl1')
    title = None
    rows = [['id1', 'integer', ' not null', 'plain', None, None],
     [
      'txt1', 'text', ' not null', 'extended', None, None]]
    headers = [
     'Column', 'Type', 'Modifiers', 'Storage', 'Stats target', 'Description']
    status = 'Indexes:\n    "id_text" PRIMARY KEY, btree (id1, txt1)\nHas OIDs: no\n'
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_d_table_with_exclusion(executor):
    results = executor('\\d tbl3')
    title = None
    rows = [['c3', 'circle', '']]
    headers = ['Column', 'Type', 'Modifiers']
    status = 'Indexes:\n    "tbl3_c3_excl" EXCLUDE USING gist (c3 WITH &&)\n'
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_dn(executor):
    """List all schemas."""
    results = executor('\\dn')
    title = None
    rows = [('public', POSTGRES_USER),
     (
      'schema1', POSTGRES_USER),
     (
      'schema2', POSTGRES_USER)]
    headers = ['Name', 'Owner']
    status = 'SELECT 3'
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_dt(executor):
    """List all tables in public schema."""
    results = executor('\\dt')
    title = None
    rows = [('public', 'tbl1', 'table', POSTGRES_USER),
     (
      'public', 'tbl2', 'table', POSTGRES_USER),
     (
      'public', 'tbl3', 'table', POSTGRES_USER)]
    headers = objects_listing_headers[:-2]
    status = 'SELECT 3'
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_dt_verbose(executor):
    """List all tables in public schema in verbose mode."""
    results = executor('\\dt+')
    title = None
    rows = [('public', 'tbl1', 'table', POSTGRES_USER, '8192 bytes', None),
     (
      'public', 'tbl2', 'table', POSTGRES_USER, '8192 bytes', None),
     (
      'public', 'tbl3', 'table', POSTGRES_USER, '0 bytes', None)]
    headers = objects_listing_headers
    status = 'SELECT 3'
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_dv(executor):
    """List all views in public schema."""
    results = executor('\\dv')
    title = None
    row = [('public', 'vw1', 'view', POSTGRES_USER)]
    headers = objects_listing_headers[:-2]
    status = 'SELECT 1'
    expected = [title, row, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_dv_verbose(executor):
    """List all views in s1 schema in verbose mode."""
    results = executor('\\dv+ schema1.*')
    title = None
    row = [('schema1', 's1_vw1', 'view', POSTGRES_USER, '0 bytes', None)]
    headers = objects_listing_headers
    status = 'SELECT 1'
    expected = [title, row, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_dm(executor):
    """List all materialized views in schema1."""
    results = executor('\\dm schema1.*')
    title = None
    row = [('schema1', 's1_mvw1', 'materialized view', POSTGRES_USER)]
    headers = objects_listing_headers[:-2]
    status = 'SELECT 1'
    expected = [title, row, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_dm_verbose(executor):
    """List all materialized views in public schema in verbose mode."""
    results = executor('\\dm+')
    title = None
    row = [('public', 'mvw1', 'materialized view', POSTGRES_USER, '8192 bytes', None)]
    headers = objects_listing_headers
    status = 'SELECT 1'
    expected = [title, row, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_ds(executor):
    """List all sequences in public schema."""
    results = executor('\\ds')
    title = None
    row = [('public', 'tbl2_id2_seq', 'sequence', POSTGRES_USER)]
    headers = objects_listing_headers[:-2]
    status = 'SELECT 1'
    expected = [title, row, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_ds_verbose(executor):
    """List all sequences in public schema in verbose mode."""
    results = executor('\\ds+')
    title = None
    row = [('public', 'tbl2_id2_seq', 'sequence', POSTGRES_USER, '8192 bytes', None)]
    headers = objects_listing_headers
    status = 'SELECT 1'
    expected = [title, row, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_di(executor):
    """List all indexes in public schema."""
    results = executor('\\di')
    title = None
    row = [('public', 'id_text', 'index', POSTGRES_USER),
     (
      'public', 'tbl3_c3_excl', 'index', POSTGRES_USER)]
    headers = objects_listing_headers[:-2]
    status = 'SELECT 2'
    expected = [title, row, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_di_verbose(executor):
    """List all indexes in public schema in verbose mode."""
    results = executor('\\di+')
    title = None
    row = [('public', 'id_text', 'index', POSTGRES_USER, '8192 bytes', None),
     (
      'public', 'tbl3_c3_excl', 'index', POSTGRES_USER, '8192 bytes', None)]
    headers = objects_listing_headers
    status = 'SELECT 2'
    expected = [title, row, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_dT(executor):
    """List all datatypes."""
    results = executor('\\dT')
    title = None
    rows = [('public', 'foo', None)]
    headers = ['Schema', 'Name', 'Description']
    status = 'SELECT 1'
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_db(executor):
    """List all tablespaces."""
    title, rows, header, status = executor('\\db')
    @py_assert1 = title is None
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (title, None)) % {'py2': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None',  'py0': @pytest_ar._saferepr(title) if 'title' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(title) else 'title'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert2 = ['Name', 'Owner', 'Location']
    @py_assert1 = header == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (header, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(header) if 'header' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(header) else 'header'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'pg_default'
    @py_assert3 = rows[0]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


@dbtest
def test_slash_db_name(executor):
    """List tablespace by name."""
    title, rows, header, status = executor('\\db pg_default')
    @py_assert1 = title is None
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py2)s', ), (title, None)) % {'py2': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None',  'py0': @pytest_ar._saferepr(title) if 'title' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(title) else 'title'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert2 = ['Name', 'Owner', 'Location']
    @py_assert1 = header == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (header, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(header) if 'header' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(header) else 'header'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = 'pg_default'
    @py_assert3 = rows[0]
    @py_assert2 = @py_assert0 in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert2 = 'SELECT 1'
    @py_assert1 = status == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (status, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(status) if 'status' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(status) else 'status'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


@dbtest
def test_slash_df(executor):
    results = executor('\\df')
    title = None
    rows = [('public', 'func1', 'integer', '', 'normal')]
    headers = ['Schema', 'Name', 'Result data type', 'Argument data types',
     'Type']
    status = 'SELECT 1'
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


help_rows = [['ABORT', 'ALTER AGGREGATE', 'ALTER COLLATION', 'ALTER CONVERSION', 'ALTER DATABASE', 'ALTER DEFAULT PRIVILEGES'], ['ALTER DOMAIN', 'ALTER EVENT TRIGGER', 'ALTER EXTENSION', 'ALTER FOREIGN DATA WRAPPER', 'ALTER FOREIGN TABLE', 'ALTER FUNCTION'], ['ALTER GROUP', 'ALTER INDEX', 'ALTER LANGUAGE', 'ALTER LARGE OBJECT', 'ALTER MATERIALIZED VIEW', 'ALTER OPCLASS'], ['ALTER OPERATOR', 'ALTER OPFAMILY', 'ALTER POLICY', 'ALTER ROLE', 'ALTER RULE', 'ALTER SCHEMA'], ['ALTER SEQUENCE', 'ALTER SERVER', 'ALTER SYSTEM', 'ALTER TABLE', 'ALTER TABLESPACE', 'ALTER TRIGGER'], ['ALTER TSCONFIG', 'ALTER TSDICTIONARY', 'ALTER TSPARSER', 'ALTER TSTEMPLATE', 'ALTER TYPE', 'ALTER USER'], ['ALTER USER MAPPING', 'ALTER VIEW', 'ANALYZE', 'BEGIN', 'CHECKPOINT', 'CLOSE'], ['CLUSTER', 'COMMENT', 'COMMIT', 'COMMIT PREPARED', 'COPY', 'CREATE AGGREGATE'], ['CREATE CAST', 'CREATE COLLATION', 'CREATE CONVERSION', 'CREATE DATABASE', 'CREATE DOMAIN', 'CREATE EVENT TRIGGER'], ['CREATE EXTENSION', 'CREATE FOREIGN DATA WRAPPER', 'CREATE FOREIGN TABLE', 'CREATE FUNCTION', 'CREATE GROUP', 'CREATE INDEX'], ['CREATE LANGUAGE', 'CREATE MATERIALIZED VIEW', 'CREATE OPCLASS', 'CREATE OPERATOR', 'CREATE OPFAMILY', 'CREATE POLICY'], ['CREATE ROLE', 'CREATE RULE', 'CREATE SCHEMA', 'CREATE SEQUENCE', 'CREATE SERVER', 'CREATE TABLE'], ['CREATE TABLE AS', 'CREATE TABLESPACE', 'CREATE TRANSFORM', 'CREATE TRIGGER', 'CREATE TSCONFIG', 'CREATE TSDICTIONARY'], ['CREATE TSPARSER', 'CREATE TSTEMPLATE', 'CREATE TYPE', 'CREATE USER', 'CREATE USER MAPPING', 'CREATE VIEW'], ['DEALLOCATE', 'DECLARE', 'DELETE', 'DISCARD', 'DO', 'DROP AGGREGATE'], ['DROP CAST', 'DROP COLLATION', 'DROP CONVERSION', 'DROP DATABASE', 'DROP DOMAIN', 'DROP EVENT TRIGGER'], ['DROP EXTENSION', 'DROP FOREIGN DATA WRAPPER', 'DROP FOREIGN TABLE', 'DROP FUNCTION', 'DROP GROUP', 'DROP INDEX'], ['DROP LANGUAGE', 'DROP MATERIALIZED VIEW', 'DROP OPCLASS', 'DROP OPERATOR', 'DROP OPFAMILY', 'DROP OWNED'], ['DROP POLICY', 'DROP ROLE', 'DROP RULE', 'DROP SCHEMA', 'DROP SEQUENCE', 'DROP SERVER'], ['DROP TABLE', 'DROP TABLESPACE', 'DROP TRANSFORM', 'DROP TRIGGER', 'DROP TSCONFIG', 'DROP TSDICTIONARY'], ['DROP TSPARSER', 'DROP TSTEMPLATE', 'DROP TYPE', 'DROP USER', 'DROP USER MAPPING', 'DROP VIEW'], ['END', 'EXECUTE', 'EXPLAIN', 'FETCH', 'GRANT', 'IMPORT FOREIGN SCHEMA'], ['INSERT', 'LISTEN', 'LOAD', 'LOCK', 'MOVE', 'NOTIFY'], ['PGBENCH', 'PREPARE', 'PREPARE TRANSACTION', 'REASSIGN OWNED', 'REFRESH MATERIALIZED VIEW', 'REINDEX'], ['RELEASE SAVEPOINT', 'RESET', 'REVOKE', 'ROLLBACK', 'ROLLBACK PREPARED', 'ROLLBACK TO'], ['SAVEPOINT', 'SECURITY LABEL', 'SELECT', 'SELECT INTO', 'SET', 'SET CONSTRAINTS'], ['SET ROLE', 'SET SESSION AUTH', 'SET TRANSACTION', 'SHOW', 'START TRANSACTION', 'TRUNCATE'], ['UNLISTEN', 'UPDATE', 'VACUUM', 'VALUES']]

@dbtest
def test_slash_h(executor):
    """List all commands."""
    results = executor('\\h')
    expected = [None, help_rows, [], None]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_h_command(executor):
    """Check help is returned for all commands"""
    for command in itertools.chain(*help_rows):
        results = executor('\\h %s' % command)
        @py_assert0 = results[3]
        @py_assert2 = @py_assert0.startswith
        @py_assert4 = 'Description\n'
        @py_assert6 = @py_assert2(@py_assert4)
        if not @py_assert6:
            @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.startswith\n}(%(py5)s)\n}') % {'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4),  'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(@py_assert0)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = 'Syntax'
        @py_assert3 = results[3]
        @py_assert2 = @py_assert0 in @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    return


@dbtest
def test_slash_h_alias(executor):
    r"""\? is properly aliased to \h"""
    h_results = executor('\\h SELECT')
    results = executor('\\? SELECT')
    @py_assert0 = results[3]
    @py_assert3 = h_results[3]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


@dbtest
def test_slash_copy_to_tsv(executor, tmpdir):
    filepath = tmpdir.join('pycons.tsv')
    executor("\\copy (SELECT 'Montréal', 'Portland', 'Cleveland') TO '{0}' ".format(filepath))
    infile = filepath.open(encoding='utf-8')
    contents = infile.read()
    @py_assert2 = contents.splitlines
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 1
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.splitlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4),  'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(contents) if 'contents' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(contents) else 'contents',  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert0 = 'Montréal'
    @py_assert2 = @py_assert0 in contents
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, contents)) % {'py3': @pytest_ar._saferepr(contents) if 'contents' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(contents) else 'contents',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


@dbtest
def test_slash_copy_to_stdout(executor, capsys):
    executor("\\copy (SELECT 'Montréal', 'Portland', 'Cleveland') TO stdout")
    out, err = capsys.readouterr()
    @py_assert2 = 'Montréal\tPortland\tCleveland\n'
    @py_assert1 = out == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (out, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(out) if 'out' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(out) else 'out'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


@dbtest
def test_slash_copy_to_csv(executor, tmpdir):
    filepath = tmpdir.join('pycons.tsv')
    executor("\\copy (SELECT 'Montréal', 'Portland', 'Cleveland') TO '{0}' WITH csv".format(filepath))
    infile = filepath.open(encoding='utf-8')
    contents = infile.read()
    @py_assert2 = contents.splitlines
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 1
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.splitlines\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9),  'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4),  'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(contents) if 'contents' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(contents) else 'contents',  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert0 = 'Montréal'
    @py_assert2 = @py_assert0 in contents
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, contents)) % {'py3': @pytest_ar._saferepr(contents) if 'contents' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(contents) else 'contents',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = ','
    @py_assert2 = @py_assert0 in contents
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, contents)) % {'py3': @pytest_ar._saferepr(contents) if 'contents' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(contents) else 'contents',  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return


@dbtest
def test_slash_copy_from_csv(executor, connection, tmpdir):
    filepath = tmpdir.join('tbl1.csv')
    executor("\\copy (SELECT 22, 'elephant') TO '{0}' WITH csv".format(filepath))
    executor("\\copy tbl1 FROM '{0}' WITH csv".format(filepath))
    cur = connection.cursor()
    cur.execute('SELECT * FROM tbl1 WHERE id1 = 22')
    row = cur.fetchone()
    @py_assert0 = row[1]
    @py_assert3 = 'elephant'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3),  'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


@dbtest
def test_slash_sf(executor):
    results = executor('\\sf func1')
    title = None
    rows = [('CREATE OR REPLACE FUNCTION public.func1()\n RETURNS integer\n LANGUAGE sql\nAS $function$select 1$function$\n', )]
    headers = [
     'source']
    status = None
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_sf_unknown(executor):
    try:
        executor('\\sf non_existing')
    except Exception as e:
        @py_assert0 = 'non_existing'
        @py_assert5 = str(e)
        @py_assert2 = @py_assert0 in @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py6)s\n{%(py6)s = %(py3)s(%(py4)s)\n}', ), (@py_assert0, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5),  'py4': @pytest_ar._saferepr(e) if 'e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(e) else 'e',  'py3': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert5 = None
    else:
        if not False:
            @py_format1 = (@pytest_ar._format_assertmsg('Expected an exception') + '\n>assert %(py0)s') % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
        return


@dbtest
def test_slash_sf_parens(executor):
    results = executor('\\sf func1()')
    title = None
    rows = [('CREATE OR REPLACE FUNCTION public.func1()\n RETURNS integer\n LANGUAGE sql\nAS $function$select 1$function$\n', )]
    headers = [
     'source']
    status = None
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


@dbtest
def test_slash_sf_verbose(executor):
    results = executor('\\sf+ schema1.s1_func1')
    title = None
    rows = [('        CREATE OR REPLACE FUNCTION schema1.s1_func1()\n         RETURNS integer\n         LANGUAGE sql\n1       AS $function$select 2$function$\n', )]
    headers = [
     'source']
    status = None
    expected = [title, rows, headers, status]
    @py_assert1 = results == expected
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (results, expected)) % {'py2': @pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py0': @pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return