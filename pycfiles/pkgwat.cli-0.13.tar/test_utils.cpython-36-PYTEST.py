# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kparal/devel/infra/pkgwat.cli/tests/test_utils.py
# Compiled at: 2019-05-27 11:59:36
# Size of source mod 2**32: 109 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pkgwat.cli.utils

def test_format_time():
    @py_assert1 = pkgwat.cli
    @py_assert3 = @py_assert1.utils
    @py_assert5 = @py_assert3._format_time
    @py_assert7 = 0
    @py_assert9 = @py_assert5(@py_assert7)
    @py_assert12 = '1970/01/01'
    @py_assert11 = @py_assert9 == @py_assert12
    if @py_assert11 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/kparal/devel/infra/pkgwat.cli/tests/test_utils.py', lineno=4)
    if not @py_assert11:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert11,), ('%(py10)s\n{%(py10)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.cli\n}.utils\n}._format_time\n}(%(py8)s)\n} == %(py13)s', ), (@py_assert9, @py_assert12)) % {'py0':@pytest_ar._saferepr(pkgwat) if 'pkgwat' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pkgwat) else 'pkgwat',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(@py_assert9),  'py13':@pytest_ar._saferepr(@py_assert12)}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert12 = None