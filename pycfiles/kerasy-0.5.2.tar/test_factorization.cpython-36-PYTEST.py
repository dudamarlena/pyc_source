# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/Bio/test_factorization.py
# Compiled at: 2020-05-10 22:03:14
# Size of source mod 2**32: 676 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.utils import generateSeq
from kerasy.Bio.factorization import simple_compression, simple_decompression
len_sequences = 100

def get_test_data():
    sequence = generateSeq(size=len_sequences, nucleic_acid='DNA',
      weights=None,
      seed=123)
    sequence = ''.join(sequence)
    return sequence


def test_simple_compression():
    sequence = get_test_data()
    compressed_string = simple_compression(sequence)
    @py_assert2 = len(sequence)
    @py_assert7 = len(compressed_string)
    @py_assert4 = @py_assert2 >= @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} >= %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}', ), (@py_assert2, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(sequence) if 'sequence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sequence) else 'sequence',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py6':@pytest_ar._saferepr(compressed_string) if 'compressed_string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(compressed_string) else 'compressed_string',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    decompressed_string = simple_decompression(compressed_string)
    @py_assert1 = decompressed_string == sequence
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (decompressed_string, sequence)) % {'py0':@pytest_ar._saferepr(decompressed_string) if 'decompressed_string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(decompressed_string) else 'decompressed_string',  'py2':@pytest_ar._saferepr(sequence) if 'sequence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sequence) else 'sequence'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None