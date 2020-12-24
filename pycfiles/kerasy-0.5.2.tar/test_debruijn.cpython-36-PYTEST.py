# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/search/test_debruijn.py
# Compiled at: 2020-05-13 01:13:30
# Size of source mod 2**32: 651 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from kerasy.search.debruijn import kmer_deBruijnGraph
from kerasy.utils import generateSeq
len_sequences = 50
num_sequecen = 100
k = 45

def get_test_data():
    sequences = generateSeq(size=(num_sequecen, len_sequences), nucleic_acid='DNA',
      weights=None,
      seed=123)
    sequences = list(map(lambda x: ''.join(x), sequences))
    return sequences


def test_kmer_debruijn(path='deBruijnGraph.png'):
    reads = get_test_data()
    model = kmer_deBruijnGraph(k=k)
    model.build(reads)
    @py_assert1 = model.export_graphviz
    @py_assert4 = @py_assert1(path)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.export_graphviz\n}(%(py3)s)\n}' % {'py0':@pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(path) if 'path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(path) else 'path',  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert4 = None
    os.remove(path)