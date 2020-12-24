# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eevee/dev/camel.git/build/lib/camel/tests/test_docs.py
# Compiled at: 2015-10-19 22:51:23
# Size of source mod 2**32: 3792 bytes
"""Make sure the documentation examples actually, uh, work."""
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, textwrap

def test_docs_table_v1():

    class Table(object):

        def __init__(self, size):
            self.size = size

        def __repr__(self):
            return '<Table {self.size!r}>'.format(self=self)

    from camel import CamelRegistry
    my_types = CamelRegistry()

    @my_types.dumper(Table, 'table', version=1)
    def _dump_table(table):
        return {'size': table.size}

    @my_types.loader('table', version=1)
    def _load_table(data, version):
        return Table(data['size'])

    from camel import Camel
    table = Table(25)
    @py_assert1 = [my_types]
    @py_assert3 = Camel(@py_assert1)
    @py_assert5 = @py_assert3.dump
    @py_assert8 = @py_assert5(table)
    @py_assert11 = '!table;1\nsize: 25\n'
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.dump\n}(%(py7)s)\n} == %(py12)s',), (@py_assert8, @py_assert11)) % {'py12': @pytest_ar._saferepr(@py_assert11), 'py0': @pytest_ar._saferepr(Camel) if 'Camel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Camel) else 'Camel', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(table) if 'table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table) else 'table', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format15 = ('' + 'assert %(py14)s') % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert11 = None
    data = {'chairs': [], 'tables': [Table(25), Table(36)]}
    @py_assert1 = [my_types]
    @py_assert3 = Camel(@py_assert1)
    @py_assert5 = @py_assert3.dump
    @py_assert8 = @py_assert5(data)
    @py_assert12 = textwrap.dedent
    @py_assert14 = '\n        chairs: []\n        tables:\n        - !table;1\n          size: 25\n        - !table;1\n          size: 36\n    '
    @py_assert16 = @py_assert12(@py_assert14)
    @py_assert18 = @py_assert16.lstrip
    @py_assert20 = @py_assert18()
    @py_assert10 = @py_assert8 == @py_assert20
    if not @py_assert10:
        @py_format22 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.dump\n}(%(py7)s)\n} == %(py21)s\n{%(py21)s = %(py19)s\n{%(py19)s = %(py17)s\n{%(py17)s = %(py13)s\n{%(py13)s = %(py11)s.dedent\n}(%(py15)s)\n}.lstrip\n}()\n}',), (@py_assert8, @py_assert20)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(Camel) if 'Camel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Camel) else 'Camel', 'py13': @pytest_ar._saferepr(@py_assert12), 'py4': @pytest_ar._saferepr(@py_assert3), 'py15': @pytest_ar._saferepr(@py_assert14), 'py7': @pytest_ar._saferepr(data) if 'data' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(data) else 'data', 'py21': @pytest_ar._saferepr(@py_assert20), 'py11': @pytest_ar._saferepr(textwrap) if 'textwrap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(textwrap) else 'textwrap', 
         'py19': @pytest_ar._saferepr(@py_assert18), 'py17': @pytest_ar._saferepr(@py_assert16), 'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format24 = ('' + 'assert %(py23)s') % {'py23': @py_format22}
        raise AssertionError(@pytest_ar._format_explanation(@py_format24))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = None
    table, = Camel([my_types]).load('[!table;1 {size: 100}]')
    @py_assert3 = isinstance(table, Table)
    if not @py_assert3:
        @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}') % {'py2': @pytest_ar._saferepr(Table) if 'Table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Table) else 'Table', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py1': @pytest_ar._saferepr(table) if 'table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table) else 'table'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert1 = table.size
    @py_assert4 = 100
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.size\n} == %(py5)s',), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(table) if 'table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table) else 'table'}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_docs_table_v2():

    class Table(object):

        def __init__(self, height, width):
            self.height = height
            self.width = width

        def __repr__(self):
            return '<Table {self.height!r}x{self.width!r}>'.format(self=self)

    from camel import Camel, CamelRegistry
    my_types = CamelRegistry()

    @my_types.dumper(Table, 'table', version=2)
    def _dump_table_v2(table):
        return {'height': table.height, 
         'width': table.width}

    @my_types.loader('table', version=2)
    def _load_table_v2(data, version):
        return Table(data['height'], data['width'])

    @my_types.loader('table', version=1)
    def _load_table_v1(data, version):
        edge = data['size'] ** 0.5
        return Table(edge, edge)

    table = Table(7, 10)
    @py_assert1 = [my_types]
    @py_assert3 = Camel(@py_assert1)
    @py_assert5 = @py_assert3.dump
    @py_assert8 = @py_assert5(table)
    @py_assert12 = textwrap.dedent
    @py_assert14 = '\n        !table;2\n        height: 7\n        width: 10\n    '
    @py_assert16 = @py_assert12(@py_assert14)
    @py_assert18 = @py_assert16.lstrip
    @py_assert20 = @py_assert18()
    @py_assert10 = @py_assert8 == @py_assert20
    if not @py_assert10:
        @py_format22 = @pytest_ar._call_reprcompare(('==',), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}.dump\n}(%(py7)s)\n} == %(py21)s\n{%(py21)s = %(py19)s\n{%(py19)s = %(py17)s\n{%(py17)s = %(py13)s\n{%(py13)s = %(py11)s.dedent\n}(%(py15)s)\n}.lstrip\n}()\n}',), (@py_assert8, @py_assert20)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(Camel) if 'Camel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Camel) else 'Camel', 'py13': @pytest_ar._saferepr(@py_assert12), 'py4': @pytest_ar._saferepr(@py_assert3), 'py15': @pytest_ar._saferepr(@py_assert14), 'py7': @pytest_ar._saferepr(table) if 'table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table) else 'table', 'py21': @pytest_ar._saferepr(@py_assert20), 'py11': @pytest_ar._saferepr(textwrap) if 'textwrap' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(textwrap) else 'textwrap', 
         'py19': @pytest_ar._saferepr(@py_assert18), 'py17': @pytest_ar._saferepr(@py_assert16), 'py2': @pytest_ar._saferepr(@py_assert1), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format24 = ('' + 'assert %(py23)s') % {'py23': @py_format22}
        raise AssertionError(@pytest_ar._format_explanation(@py_format24))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = @py_assert20 = None

    @my_types.dumper(Table, 'table', version=1)
    def _dump_table_v1(table):
        return {'size': table.height * table.width}

    camel = Camel([my_types])
    camel.lock_version(Table, 1)
    @py_assert1 = camel.dump
    @py_assert4 = 5
    @py_assert6 = 7
    @py_assert8 = Table(@py_assert4, @py_assert6)
    @py_assert10 = @py_assert1(@py_assert8)
    @py_assert13 = '!table;1\nsize: 35\n'
    @py_assert12 = @py_assert10 == @py_assert13
    if not @py_assert12:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.dump\n}(%(py9)s\n{%(py9)s = %(py3)s(%(py5)s, %(py7)s)\n})\n} == %(py14)s',), (@py_assert10, @py_assert13)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py14': @pytest_ar._saferepr(@py_assert13), 'py0': @pytest_ar._saferepr(camel) if 'camel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(camel) else 'camel', 'py3': @pytest_ar._saferepr(Table) if 'Table' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Table) else 'Table', 'py11': @pytest_ar._saferepr(@py_assert10), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format17 = ('' + 'assert %(py16)s') % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = None


def test_docs_deleted():

    class DummyData(object):

        def __init__(self, data):
            self.data = data

    from camel import Camel, CamelRegistry
    my_types = CamelRegistry()

    @my_types.loader('deleted-type', version=all)
    def _load_deleted_type(data, version):
        return DummyData(data)

    camel = Camel([my_types])
    @py_assert2 = camel.load
    @py_assert4 = '!deleted-type;4 foo'
    @py_assert6 = @py_assert2(@py_assert4)
    @py_assert9 = isinstance(@py_assert6, DummyData)
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.load\n}(%(py5)s)\n}, %(py8)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(camel) if 'camel' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(camel) else 'camel', 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(DummyData) if 'DummyData' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DummyData) else 'DummyData', 'py7': @pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert9 = None


def test_docs_table_any():

    class Table(object):

        def __init__(self, height, width):
            self.height = height
            self.width = width

        def __repr__(self):
            return '<Table {self.height!r}x{self.width!r}>'.format(self=self)

    from camel import Camel, CamelRegistry
    my_types = CamelRegistry()

    @my_types.loader('table', version=any)
    def _load_table(data, version):
        if 'size' in data:
            edge = data['size'] ** 0.5
            return Table(edge, edge)
        else:
            return Table(data['height'], data['width'])

    camel = Camel([my_types])
    table1, table2 = camel.load('[!table;1 {size: 49}, !table;2 {height: 5, width: 9}]')
    @py_assert1 = table1.height
    @py_assert4 = 7
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.height\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(table1) if 'table1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table1) else 'table1'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = table1.width
    @py_assert4 = 7
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.width\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(table1) if 'table1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table1) else 'table1'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = table2.height
    @py_assert4 = 5
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.height\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(table2) if 'table2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table2) else 'table2'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = table2.width
    @py_assert4 = 9
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.width\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(table2) if 'table2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(table2) else 'table2'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None