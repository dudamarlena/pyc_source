# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/search/test_trie.py
# Compiled at: 2020-05-13 01:50:13
# Size of source mod 2**32: 752 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.search.trie import NaiveTrie, LOUDSTrieOffline
from kerasy.utils import generateSeq
len_sequences = 50
num_sequecen = 100

def get_test_data():
    sequences = generateSeq(size=(num_sequecen, len_sequences), nucleic_acid='DNA',
      weights=None,
      seed=123)
    sequences = list(map(lambda x: ''.join(x), sequences))
    return sequences


def test_louds_trie():
    sequences = get_test_data()
    louds_trie = LOUDSTrieOffline(sequences)
    @py_assert1 = [seq in louds_trie for seq in sequences]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None


def test_naive_trie():
    sequences = get_test_data()
    naive_trie = NaiveTrie(sequences)
    @py_assert1 = [seq in naive_trie for seq in sequences]
    @py_assert3 = all(@py_assert1)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n}' % {'py0':@pytest_ar._saferepr(all) if 'all' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(all) else 'all',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None