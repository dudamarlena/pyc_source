# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/core/test_system.py
# Compiled at: 2013-10-31 06:07:30
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from mio.version import version

def test_args(mio):
    @py_assert1 = mio.eval
    @py_assert3 = 'System args'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = []
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    return


def test_version(mio):
    @py_assert1 = mio.eval
    @py_assert3 = 'System version'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = @py_assert5 == version
    if not @py_assert7:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.eval\n}(%(py4)s)\n} == %(py8)s', ), (@py_assert5, version)) % {'py0': @pytest_ar._saferepr(mio) if 'mio' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mio) else 'mio', 'py8': @pytest_ar._saferepr(version) if 'version' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(version) else 'version', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    return


def test_exit(mio):
    try:
        mio.eval('System exit()')
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except SystemExit as e:
        @py_assert0 = e.args[0]
        @py_assert3 = 0
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    return


def test_exit_status(mio):
    try:
        mio.eval('System exit(1)')
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except SystemExit as e:
        @py_assert0 = e.args[0]
        @py_assert3 = 1
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    return