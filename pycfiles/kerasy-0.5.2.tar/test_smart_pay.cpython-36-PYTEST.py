# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/search/test_smart_pay.py
# Compiled at: 2020-05-13 01:35:19
# Size of source mod 2**32: 474 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.search import smart_pay
limits = [0, 1, 2, 4, 8]

def test_smart_pay():
    for i, limit in enumerate(sorted(limits)):
        combs = smart_pay(coins=[1000, 500, 100, 50, 10, 5, 1], total=7332,
          limit=limit,
          retval=True,
          verbose=(-1))
        num_coins = len(combs)
        @py_assert1 = []
        @py_assert4 = 0
        @py_assert3 = i == @py_assert4
        @py_assert0 = @py_assert3
        if not @py_assert3:
            @py_assert10 = num_coins <= prev_num_coins
            @py_assert0 = @py_assert10
        if not @py_assert0:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s == %(py5)s', ), (i, @py_assert4)) % {'py2':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = '%(py7)s' % {'py7': @py_format6}
            @py_assert1.append(@py_format8)
            if not @py_assert3:
                @py_format12 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert10,), ('%(py9)s <= %(py11)s', ), (num_coins, prev_num_coins)) % {'py9':@pytest_ar._saferepr(num_coins) if 'num_coins' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_coins) else 'num_coins',  'py11':@pytest_ar._saferepr(prev_num_coins) if 'prev_num_coins' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(prev_num_coins) else 'prev_num_coins'}
                @py_format14 = '%(py13)s' % {'py13': @py_format12}
                @py_assert1.append(@py_format14)
            @py_format15 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
            @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
            raise AssertionError(@pytest_ar._format_explanation(@py_format17))
        @py_assert0 = @py_assert1 = @py_assert3 = @py_assert4 = @py_assert10 = None
        prev_num_coins = num_coins