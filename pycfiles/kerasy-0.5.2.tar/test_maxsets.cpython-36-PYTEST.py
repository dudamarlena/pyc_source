# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/Bio/test_maxsets.py
# Compiled at: 2020-05-11 01:32:36
# Size of source mod 2**32: 776 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from kerasy.utils import generateSeq
from kerasy.Bio.maxsets import MSS
len_array = 1000

def get_test_data():
    rnd = np.random.RandomState(123)
    R_int = rnd.randint(low=(-10), high=100, size=len_array)
    R_float = rnd.uniform(low=(-10), high=100, size=len_array)
    return (R_int, R_float)


def _test_maxsets(R, limits=(5, 10)):
    model = MSS()
    for i, limit in enumerate(sorted(limits)):
        model.run(R, limit=limit, verbose=(-1))
        score = model.score
        @py_assert1 = []
        @py_assert4 = 0
        @py_assert3 = i == @py_assert4
        @py_assert0 = @py_assert3
        if not @py_assert3:
            @py_assert10 = prev_score >= score
            @py_assert0 = @py_assert10
        if not @py_assert0:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s == %(py5)s', ), (i, @py_assert4)) % {'py2':@pytest_ar._saferepr(i) if 'i' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(i) else 'i',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = '%(py7)s' % {'py7': @py_format6}
            @py_assert1.append(@py_format8)
            if not @py_assert3:
                @py_format12 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert10,), ('%(py9)s >= %(py11)s', ), (prev_score, score)) % {'py9':@pytest_ar._saferepr(prev_score) if 'prev_score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(prev_score) else 'prev_score',  'py11':@pytest_ar._saferepr(score) if 'score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(score) else 'score'}
                @py_format14 = '%(py13)s' % {'py13': @py_format12}
                @py_assert1.append(@py_format14)
            @py_format15 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
            @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
            raise AssertionError(@pytest_ar._format_explanation(@py_format17))
        @py_assert0 = @py_assert1 = @py_assert3 = @py_assert4 = @py_assert10 = None
        prev_score = score


def test_maxsets_int():
    R_int, _ = get_test_data()
    _test_maxsets(R_int, limits=(5, 10))


def test_maxsets_float():
    _, R_float = get_test_data()
    _test_maxsets(R_float, limits=(5, 10))