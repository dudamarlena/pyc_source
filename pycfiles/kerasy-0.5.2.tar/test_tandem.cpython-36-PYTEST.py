# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/Bio/test_tandem.py
# Compiled at: 2020-05-11 01:24:56
# Size of source mod 2**32: 771 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.Bio.tandem import find_tandem
from kerasy.utils import generateSeq
len_sequences = 1000

def get_test_data():
    sequence = generateSeq(size=len_sequences, nucleic_acid='DNA',
      weights=None,
      seed=123)
    sequence = ''.join(sequence)
    return sequence


def test_find_tandem():
    sequence = get_test_data()
    max_val_sais, tandem_lists_sais = find_tandem(sequence, method='SAIS')
    tandem_sais = tandem_lists_sais[0]
    max_val_dp, tandem_lists_dp = find_tandem(sequence, method='DP')
    tandem_dp = tandem_lists_dp[0]
    @py_assert1 = max_val_sais == max_val_dp
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (max_val_sais, max_val_dp)) % {'py0':@pytest_ar._saferepr(max_val_sais) if 'max_val_sais' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(max_val_sais) else 'max_val_sais',  'py2':@pytest_ar._saferepr(max_val_dp) if 'max_val_dp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(max_val_dp) else 'max_val_dp'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = [tandem_dp[i:] + tandem_dp[:i] == tandem_sais for i in range(len(tandem_dp))]
    @py_assert3 = any(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(any) if 'any' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(any) else 'any',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None