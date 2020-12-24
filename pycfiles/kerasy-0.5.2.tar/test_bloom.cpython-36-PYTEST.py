# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/search/test_bloom.py
# Compiled at: 2020-05-13 01:09:53
# Size of source mod 2**32: 602 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.search.bloom import BloomFilter
from kerasy.utils import generateSeq
len_sequences = 50
num_sequecen = 1000

def get_test_data():
    reads = generateSeq(size=(num_sequecen, len_sequences), nucleic_acid='DNA',
      weights=None,
      seed=123)
    reads = list(map(lambda x: ''.join(x), reads))
    return reads


def test_bloom_filter():
    reads = get_test_data()
    bf = BloomFilter(num_sequecen, error_rate=0.001)
    for read in reads:
        bf.add(read)

    @py_assert1 = [read in bf for read in reads]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None