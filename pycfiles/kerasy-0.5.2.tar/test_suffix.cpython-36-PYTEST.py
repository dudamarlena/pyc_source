# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/Bio/test_suffix.py
# Compiled at: 2020-05-11 01:29:00
# Size of source mod 2**32: 664 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from kerasy.Bio.string import ALPHABETS
from kerasy.Bio.suffix import SAIS, BWT_create, reverseBWT
len_string = 100000

def get_test_data():
    rnd = np.random.RandomState(1)
    string = ''.join(rnd.choice(ALPHABETS, len_string))
    return string


def test_SAIS():
    input = 'abaabababbabbb'
    answer = np.asarray([14, 2, 0, 3, 5, 7, 10, 13, 1, 4, 6, 9, 12, 8, 11])
    SA = SAIS(input)
    @py_assert1 = np.all
    @py_assert4 = SA == answer
    @py_assert8 = @py_assert1(@py_assert4)
    if not @py_assert8:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s == %(py5)s', ), (SA, answer)) % {'py3':@pytest_ar._saferepr(SA) if 'SA' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SA) else 'SA',  'py5':@pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer'}
        @py_format10 = 'assert %(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.all\n}(%(py7)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py7':@py_format6,  'py9':@pytest_ar._saferepr(@py_assert8)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert8 = None


def test_burrows_wheeler_transform():
    string = get_test_data()
    SA = SAIS(string)
    bwt = BWT_create(string, SA)
    reversed_bwt = reverseBWT(bwt)
    @py_assert1 = reversed_bwt == string
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (reversed_bwt, string)) % {'py0':@pytest_ar._saferepr(reversed_bwt) if 'reversed_bwt' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(reversed_bwt) else 'reversed_bwt',  'py2':@pytest_ar._saferepr(string) if 'string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(string) else 'string'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None