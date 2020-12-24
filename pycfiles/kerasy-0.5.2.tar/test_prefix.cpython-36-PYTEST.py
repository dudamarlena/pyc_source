# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/Bio/test_prefix.py
# Compiled at: 2020-05-11 01:31:24
# Size of source mod 2**32: 1096 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from kerasy.utils import generateSeq
from kerasy.Bio.prefix import LCP_create, LP_create, LP_with_pattern_create
len_text = 100
len_pattern = 10

def get_test_data(len_sequences):
    sequence = generateSeq(size=len_sequences, nucleic_acid='DNA',
      weights=None,
      seed=(123 + len_sequences))
    sequence = ''.join(sequence)
    return sequence


def test_LCP_create():
    input = 'banana'
    answer = np.asarray([0, 1, 3, 0, 0, 2, -1])
    lcp_array = LCP_create(input)
    @py_assert1 = np.all
    @py_assert4 = lcp_array == answer
    @py_assert8 = @py_assert1(@py_assert4)
    if not @py_assert8:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s == %(py5)s', ), (lcp_array, answer)) % {'py3':@pytest_ar._saferepr(lcp_array) if 'lcp_array' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(lcp_array) else 'lcp_array',  'py5':@pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer'}
        @py_format10 = 'assert %(py9)s\n{%(py9)s = %(py2)s\n{%(py2)s = %(py0)s.all\n}(%(py7)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py7':@py_format6,  'py9':@pytest_ar._saferepr(@py_assert8)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert8 = None


def test_LP_create():
    text = get_test_data(len_text)
    lp_array = LP_create(text)
    @py_assert1 = [text[:lp] == text[i:i + lp] for i, lp in enumerate(lp_array)]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_LP_with_pattern_create():
    text = get_test_data(len_text)
    pattern = get_test_data(len_pattern)
    lp_with_pattern = LP_with_pattern_create(pattern, text)
    @py_assert1 = [text[i:i + lp] == pattern[:lp] for i, lp in enumerate(lp_with_pattern)]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None