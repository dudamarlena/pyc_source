# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\test\test_content.py
# Compiled at: 2016-01-04 11:02:19
# Size of source mod 2**32: 3856 bytes
"""Test of content synchronization of KEP backend."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from unittest import mock
from jep_py.content import ContentMonitor, SynchronizationResult, NewlineMode

def test_content_empty():
    monitor = ContentMonitor()
    @py_assert0 = monitor[mock.sentinel.UNKNOWN_FILE]
    @py_assert3 = None
    @py_assert2 = @py_assert0 is @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py4)s', ), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_initial_sync():
    monitor = ContentMonitor()
    @py_assert1 = monitor.synchronize
    @py_assert4 = mock.sentinel
    @py_assert6 = @py_assert4.FILEPATH
    @py_assert8 = 'This is the string.'
    @py_assert10 = 0
    @py_assert12 = @py_assert1(@py_assert6, @py_assert8, @py_assert10)
    @py_assert16 = SynchronizationResult.Updated
    @py_assert14 = @py_assert12 == @py_assert16
    if not @py_assert14:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.synchronize\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.sentinel\n}.FILEPATH\n}, %(py9)s, %(py11)s)\n} == %(py17)s\n{%(py17)s = %(py15)s.Updated\n}',), (@py_assert12, @py_assert16)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(SynchronizationResult) if 'SynchronizationResult' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SynchronizationResult) else 'SynchronizationResult', 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(monitor) if 'monitor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(monitor) else 'monitor', 'py3': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock'}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = monitor[mock.sentinel.FILEPATH]
    @py_assert3 = 'This is the string.'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_replace_all():
    monitor = ContentMonitor()
    monitor.synchronize(mock.sentinel.FILEPATH, 'This is the string.', 0)
    @py_assert1 = monitor.synchronize
    @py_assert4 = mock.sentinel
    @py_assert6 = @py_assert4.FILEPATH
    @py_assert8 = 'Something else'
    @py_assert10 = 0
    @py_assert12 = @py_assert1(@py_assert6, @py_assert8, @py_assert10)
    @py_assert16 = SynchronizationResult.Updated
    @py_assert14 = @py_assert12 == @py_assert16
    if not @py_assert14:
        @py_format18 = @pytest_ar._call_reprcompare(('==',), (@py_assert14,), ('%(py13)s\n{%(py13)s = %(py2)s\n{%(py2)s = %(py0)s.synchronize\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.sentinel\n}.FILEPATH\n}, %(py9)s, %(py11)s)\n} == %(py17)s\n{%(py17)s = %(py15)s.Updated\n}',), (@py_assert12, @py_assert16)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py17': @pytest_ar._saferepr(@py_assert16), 'py15': @pytest_ar._saferepr(SynchronizationResult) if 'SynchronizationResult' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SynchronizationResult) else 'SynchronizationResult', 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(monitor) if 'monitor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(monitor) else 'monitor', 'py3': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock'}
        @py_format20 = ('' + 'assert %(py19)s') % {'py19': @py_format18}
        raise AssertionError(@pytest_ar._format_explanation(@py_format20))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = None
    @py_assert0 = monitor[mock.sentinel.FILEPATH]
    @py_assert3 = 'Something else'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_replace_part():
    monitor = ContentMonitor()
    monitor.synchronize(mock.sentinel.FILEPATH, 'This is the string.', 0)
    @py_assert1 = monitor.synchronize
    @py_assert4 = mock.sentinel
    @py_assert6 = @py_assert4.FILEPATH
    @py_assert8 = 'WAS'
    @py_assert10 = 5
    @py_assert12 = 7
    @py_assert14 = @py_assert1(@py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert18 = SynchronizationResult.Updated
    @py_assert16 = @py_assert14 == @py_assert18
    if not @py_assert16:
        @py_format20 = @pytest_ar._call_reprcompare(('==',), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.synchronize\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.sentinel\n}.FILEPATH\n}, %(py9)s, %(py11)s, %(py13)s)\n} == %(py19)s\n{%(py19)s = %(py17)s.Updated\n}',), (@py_assert14, @py_assert18)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py19': @pytest_ar._saferepr(@py_assert18), 'py17': @pytest_ar._saferepr(SynchronizationResult) if 'SynchronizationResult' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SynchronizationResult) else 'SynchronizationResult', 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(monitor) if 'monitor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(monitor) else 'monitor', 'py3': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock'}
        @py_format22 = ('' + 'assert %(py21)s') % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert0 = monitor[mock.sentinel.FILEPATH]
    @py_assert3 = 'This WAS the string.'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_insert_beginning():
    monitor = ContentMonitor()
    monitor.synchronize(mock.sentinel.FILEPATH, 'This is the string.', 0)
    @py_assert1 = monitor.synchronize
    @py_assert4 = mock.sentinel
    @py_assert6 = @py_assert4.FILEPATH
    @py_assert8 = 'Listen: '
    @py_assert10 = 0
    @py_assert12 = 0
    @py_assert14 = @py_assert1(@py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert18 = SynchronizationResult.Updated
    @py_assert16 = @py_assert14 == @py_assert18
    if not @py_assert16:
        @py_format20 = @pytest_ar._call_reprcompare(('==',), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.synchronize\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.sentinel\n}.FILEPATH\n}, %(py9)s, %(py11)s, %(py13)s)\n} == %(py19)s\n{%(py19)s = %(py17)s.Updated\n}',), (@py_assert14, @py_assert18)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py19': @pytest_ar._saferepr(@py_assert18), 'py17': @pytest_ar._saferepr(SynchronizationResult) if 'SynchronizationResult' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SynchronizationResult) else 'SynchronizationResult', 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(monitor) if 'monitor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(monitor) else 'monitor', 'py3': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock'}
        @py_format22 = ('' + 'assert %(py21)s') % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert0 = monitor[mock.sentinel.FILEPATH]
    @py_assert3 = 'Listen: This is the string.'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_append():
    monitor = ContentMonitor()
    monitor.synchronize(mock.sentinel.FILEPATH, 'This is the string.', 0)
    @py_assert1 = monitor.synchronize
    @py_assert4 = mock.sentinel
    @py_assert6 = @py_assert4.FILEPATH
    @py_assert8 = ' Really!'
    @py_assert10 = 19
    @py_assert12 = 19
    @py_assert14 = @py_assert1(@py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert18 = SynchronizationResult.Updated
    @py_assert16 = @py_assert14 == @py_assert18
    if not @py_assert16:
        @py_format20 = @pytest_ar._call_reprcompare(('==',), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.synchronize\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.sentinel\n}.FILEPATH\n}, %(py9)s, %(py11)s, %(py13)s)\n} == %(py19)s\n{%(py19)s = %(py17)s.Updated\n}',), (@py_assert14, @py_assert18)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py19': @pytest_ar._saferepr(@py_assert18), 'py17': @pytest_ar._saferepr(SynchronizationResult) if 'SynchronizationResult' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SynchronizationResult) else 'SynchronizationResult', 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(monitor) if 'monitor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(monitor) else 'monitor', 'py3': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock'}
        @py_format22 = ('' + 'assert %(py21)s') % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert0 = monitor[mock.sentinel.FILEPATH]
    @py_assert3 = 'This is the string. Really!'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_out_of_sync():
    monitor = ContentMonitor()
    monitor.synchronize(mock.sentinel.FILEPATH, 'This is the string.', 0)
    @py_assert1 = monitor.synchronize
    @py_assert4 = mock.sentinel
    @py_assert6 = @py_assert4.FILEPATH
    @py_assert8 = ' Really!'
    @py_assert10 = 20
    @py_assert12 = 22
    @py_assert14 = @py_assert1(@py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert18 = SynchronizationResult.OutOfSync
    @py_assert16 = @py_assert14 == @py_assert18
    if not @py_assert16:
        @py_format20 = @pytest_ar._call_reprcompare(('==',), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.synchronize\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.sentinel\n}.FILEPATH\n}, %(py9)s, %(py11)s, %(py13)s)\n} == %(py19)s\n{%(py19)s = %(py17)s.OutOfSync\n}',), (@py_assert14, @py_assert18)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py19': @pytest_ar._saferepr(@py_assert18), 'py17': @pytest_ar._saferepr(SynchronizationResult) if 'SynchronizationResult' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SynchronizationResult) else 'SynchronizationResult', 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(monitor) if 'monitor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(monitor) else 'monitor', 'py3': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock'}
        @py_format22 = ('' + 'assert %(py21)s') % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert0 = monitor[mock.sentinel.FILEPATH]
    @py_assert3 = 'This is the string.'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = monitor.synchronize
    @py_assert4 = mock.sentinel
    @py_assert6 = @py_assert4.FILEPATH
    @py_assert8 = ' Really!'
    @py_assert10 = 10
    @py_assert12 = 9
    @py_assert14 = @py_assert1(@py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert18 = SynchronizationResult.OutOfSync
    @py_assert16 = @py_assert14 == @py_assert18
    if not @py_assert16:
        @py_format20 = @pytest_ar._call_reprcompare(('==',), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py2)s\n{%(py2)s = %(py0)s.synchronize\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.sentinel\n}.FILEPATH\n}, %(py9)s, %(py11)s, %(py13)s)\n} == %(py19)s\n{%(py19)s = %(py17)s.OutOfSync\n}',), (@py_assert14, @py_assert18)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py19': @pytest_ar._saferepr(@py_assert18), 'py17': @pytest_ar._saferepr(SynchronizationResult) if 'SynchronizationResult' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SynchronizationResult) else 'SynchronizationResult', 'py15': @pytest_ar._saferepr(@py_assert14), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(monitor) if 'monitor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(monitor) else 'monitor', 'py3': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock'}
        @py_format22 = ('' + 'assert %(py21)s') % {'py21': @py_format20}
        raise AssertionError(@pytest_ar._format_explanation(@py_format22))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert18 = None
    @py_assert0 = monitor[mock.sentinel.FILEPATH]
    @py_assert3 = 'This is the string.'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = monitor.synchronize
    @py_assert4 = mock.sentinel
    @py_assert6 = @py_assert4.FILEPATH
    @py_assert8 = ' Really!'
    @py_assert10 = 1
    @py_assert12 = -@py_assert10
    @py_assert13 = 5
    @py_assert15 = @py_assert1(@py_assert6, @py_assert8, @py_assert12, @py_assert13)
    @py_assert19 = SynchronizationResult.OutOfSync
    @py_assert17 = @py_assert15 == @py_assert19
    if not @py_assert17:
        @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert17,), ('%(py16)s\n{%(py16)s = %(py2)s\n{%(py2)s = %(py0)s.synchronize\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.sentinel\n}.FILEPATH\n}, %(py9)s, -%(py11)s, %(py14)s)\n} == %(py20)s\n{%(py20)s = %(py18)s.OutOfSync\n}',), (@py_assert15, @py_assert19)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py14': @pytest_ar._saferepr(@py_assert13), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(monitor) if 'monitor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(monitor) else 'monitor', 'py20': @pytest_ar._saferepr(@py_assert19), 'py3': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py16': @pytest_ar._saferepr(@py_assert15), 'py18': @pytest_ar._saferepr(SynchronizationResult) if 'SynchronizationResult' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SynchronizationResult) else 'SynchronizationResult'}
        @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = None
    @py_assert0 = monitor[mock.sentinel.FILEPATH]
    @py_assert3 = 'This is the string.'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = monitor.synchronize
    @py_assert4 = mock.sentinel
    @py_assert6 = @py_assert4.FILEPATH
    @py_assert8 = ' Really!'
    @py_assert10 = 0
    @py_assert12 = 1
    @py_assert14 = -@py_assert12
    @py_assert15 = @py_assert1(@py_assert6, @py_assert8, @py_assert10, @py_assert14)
    @py_assert19 = SynchronizationResult.OutOfSync
    @py_assert17 = @py_assert15 == @py_assert19
    if not @py_assert17:
        @py_format21 = @pytest_ar._call_reprcompare(('==',), (@py_assert17,), ('%(py16)s\n{%(py16)s = %(py2)s\n{%(py2)s = %(py0)s.synchronize\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.sentinel\n}.FILEPATH\n}, %(py9)s, %(py11)s, -%(py13)s)\n} == %(py20)s\n{%(py20)s = %(py18)s.OutOfSync\n}',), (@py_assert15, @py_assert19)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py13': @pytest_ar._saferepr(@py_assert12), 'py20': @pytest_ar._saferepr(@py_assert19), 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(monitor) if 'monitor' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(monitor) else 'monitor', 'py3': @pytest_ar._saferepr(mock) if 'mock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock) else 'mock', 'py16': @pytest_ar._saferepr(@py_assert15), 'py18': @pytest_ar._saferepr(SynchronizationResult) if 'SynchronizationResult' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SynchronizationResult) else 'SynchronizationResult'}
        @py_format23 = ('' + 'assert %(py22)s') % {'py22': @py_format21}
        raise AssertionError(@pytest_ar._format_explanation(@py_format23))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert15 = @py_assert17 = @py_assert19 = None
    @py_assert0 = monitor[mock.sentinel.FILEPATH]
    @py_assert3 = 'This is the string.'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py4': @pytest_ar._saferepr(@py_assert3), 'py1': @pytest_ar._saferepr(@py_assert0)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_newline_mode_detect():
    @py_assert1 = NewlineMode.detect
    @py_assert3 = None
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = NewlineMode.Unknown
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.Unknown\n}',), (@py_assert5, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = NewlineMode.detect
    @py_assert3 = ''
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = NewlineMode.Unknown
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.Unknown\n}',), (@py_assert5, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = NewlineMode.detect
    @py_assert3 = 'Hello'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = NewlineMode.Unknown
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.Unknown\n}',), (@py_assert5, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = NewlineMode.detect
    @py_assert3 = 'Hello\n'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = NewlineMode.N
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.N\n}',), (@py_assert5, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = NewlineMode.detect
    @py_assert3 = '\nHello'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = NewlineMode.N
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.N\n}',), (@py_assert5, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = NewlineMode.detect
    @py_assert3 = 'He\nllo'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = NewlineMode.N
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.N\n}',), (@py_assert5, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = NewlineMode.detect
    @py_assert3 = 'He\nllo\n'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = NewlineMode.N
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.N\n}',), (@py_assert5, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = NewlineMode.detect
    @py_assert3 = 'He\nllo\n '
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = NewlineMode.N
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.N\n}',), (@py_assert5, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = NewlineMode.detect
    @py_assert3 = 'Hello\r'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = NewlineMode.R
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.R\n}',), (@py_assert5, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = NewlineMode.detect
    @py_assert3 = 'Hello\r\n'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = NewlineMode.RN
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s.RN\n}',), (@py_assert5, @py_assert9)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = NewlineMode.detect
    @py_assert3 = '\rHello\n'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = NewlineMode.R
    @py_assert12 = NewlineMode.N
    @py_assert14 = @py_assert9 | @py_assert12
    @py_assert7 = @py_assert5 == @py_assert14
    if not @py_assert7:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == (%(py10)s\n{%(py10)s = %(py8)s.R\n} | %(py13)s\n{%(py13)s = %(py11)s.N\n})',), (@py_assert5, @py_assert14)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py11': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py8': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format17 = ('' + 'assert %(py16)s') % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None
    @py_assert1 = NewlineMode.detect
    @py_assert3 = '\r\nHello\n'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = NewlineMode.RN
    @py_assert12 = NewlineMode.N
    @py_assert14 = @py_assert9 | @py_assert12
    @py_assert7 = @py_assert5 == @py_assert14
    if not @py_assert7:
        @py_format15 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == (%(py10)s\n{%(py10)s = %(py8)s.RN\n} | %(py13)s\n{%(py13)s = %(py11)s.N\n})',), (@py_assert5, @py_assert14)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py4': @pytest_ar._saferepr(@py_assert3), 'py10': @pytest_ar._saferepr(@py_assert9), 'py11': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py8': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py13': @pytest_ar._saferepr(@py_assert12), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format17 = ('' + 'assert %(py16)s') % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert12 = @py_assert14 = None
    @py_assert1 = NewlineMode.detect
    @py_assert3 = '\r\nHel\rlo\n'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert10 = NewlineMode.RN
    @py_assert13 = NewlineMode.N
    @py_assert15 = @py_assert10 | @py_assert13
    @py_assert17 = NewlineMode.R
    @py_assert19 = @py_assert15 | @py_assert17
    @py_assert7 = @py_assert5 == @py_assert19
    @py_assert21 = NewlineMode.All
    @py_assert8 = @py_assert19 == @py_assert21
    if not (@py_assert7 and @py_assert8):
        @py_format23 = @pytest_ar._call_reprcompare(('==', '=='), (@py_assert7, @py_assert8), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.detect\n}(%(py4)s)\n} == ((%(py11)s\n{%(py11)s = %(py9)s.RN\n} | %(py14)s\n{%(py14)s = %(py12)s.N\n}) | %(py18)s\n{%(py18)s = %(py16)s.R\n})', '((%(py11)s\n{%(py11)s = %(py9)s.RN\n} | %(py14)s\n{%(py14)s = %(py12)s.N\n}) | %(py18)s\n{%(py18)s = %(py16)s.R\n}) == %(py22)s\n{%(py22)s = %(py20)s.All\n}'), (@py_assert5, @py_assert19, @py_assert21)) % {'py12': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py11': @pytest_ar._saferepr(@py_assert10), 'py14': @pytest_ar._saferepr(@py_assert13), 'py16': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py2': @pytest_ar._saferepr(@py_assert1), 'py18': @pytest_ar._saferepr(@py_assert17), 'py22': @pytest_ar._saferepr(@py_assert21), 'py4': @pytest_ar._saferepr(@py_assert3), 'py20': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py9': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format25 = ('' + 'assert %(py24)s') % {'py24': @py_format23}
        raise AssertionError(@pytest_ar._format_explanation(@py_format25))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = @py_assert10 = @py_assert13 = @py_assert15 = @py_assert17 = @py_assert19 = @py_assert21 = None


def test_newline_mode_open_mode():
    @py_assert1 = NewlineMode.open_newline_mode
    @py_assert4 = NewlineMode.N
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = None
    @py_assert8 = @py_assert6 is @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.open_newline_mode\n}(%(py5)s\n{%(py5)s = %(py3)s.N\n})\n} is %(py10)s', ), (@py_assert6, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py3': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = NewlineMode.open_newline_mode
    @py_assert4 = NewlineMode.R
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = '\r'
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.open_newline_mode\n}(%(py5)s\n{%(py5)s = %(py3)s.R\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py3': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = NewlineMode.open_newline_mode
    @py_assert4 = NewlineMode.RN
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = '\r\n'
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.open_newline_mode\n}(%(py5)s\n{%(py5)s = %(py3)s.RN\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py3': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = NewlineMode.open_newline_mode
    @py_assert4 = NewlineMode.All
    @py_assert6 = @py_assert1(@py_assert4)
    @py_assert9 = ''
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.open_newline_mode\n}(%(py5)s\n{%(py5)s = %(py3)s.All\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4), 'py2': @pytest_ar._saferepr(@py_assert1), 'py7': @pytest_ar._saferepr(@py_assert6), 'py10': @pytest_ar._saferepr(@py_assert9), 'py0': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode', 'py3': @pytest_ar._saferepr(NewlineMode) if 'NewlineMode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NewlineMode) else 'NewlineMode'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None