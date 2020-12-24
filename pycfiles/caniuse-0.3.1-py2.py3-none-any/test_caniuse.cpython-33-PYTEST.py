# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lord63/code/caniuse/build/lib/caniuse/test/test_caniuse.py
# Compiled at: 2015-05-27 08:47:53
# Size of source mod 2**32: 582 bytes
from __future__ import absolute_import, unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from caniuse.main import check

def test_package_name_has_been_used():
    @py_assert0 = 'Sorry'
    @py_assert4 = 'requests'
    @py_assert6 = check(@py_assert4)
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0),  'py3': @pytest_ar._saferepr(check) if 'check' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check) else 'check',  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'Sorry'
    @py_assert4 = 'flask'
    @py_assert6 = check(@py_assert4)
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0),  'py3': @pytest_ar._saferepr(check) if 'check' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check) else 'check',  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'Sorry'
    @py_assert4 = 'pip'
    @py_assert6 = check(@py_assert4)
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0),  'py3': @pytest_ar._saferepr(check) if 'check' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check) else 'check',  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return


def test_package_name_has_not_been_used():
    @py_assert0 = 'Congratulation'
    @py_assert4 = 'this_package_name_has_not_been_used'
    @py_assert6 = check(@py_assert4)
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0),  'py3': @pytest_ar._saferepr(check) if 'check' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check) else 'check',  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'Congratulation'
    @py_assert4 = 'you_will_never_use_this_package_name'
    @py_assert6 = check(@py_assert4)
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0),  'py3': @pytest_ar._saferepr(check) if 'check' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check) else 'check',  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'Congratulation'
    @py_assert4 = 'I_suck_and_my_tests_are_order_dependent'
    @py_assert6 = check(@py_assert4)
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0),  'py3': @pytest_ar._saferepr(check) if 'check' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check) else 'check',  'py5': @pytest_ar._saferepr(@py_assert4),  'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    return