# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/git/jwalk/tests/test_jwalk.py
# Compiled at: 2017-04-21 21:26:24
# Size of source mod 2**32: 5488 bytes
"""py.test unittests"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, tempfile
try:
    from unittest import mock
except ImportError:
    import mock

import numpy as np, scipy.sparse as sps
from jwalk import corpus
from jwalk import graph
from jwalk import io
from jwalk import skipgram
from jwalk import __main__
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
KARATE_EDGELIST = os.path.join(DIR_PATH, 'data/karate.edgelist')
KARATE_EMBEDDINGS = os.path.join(DIR_PATH, 'data/karate.embeddings')
KARATE_GRAPH = os.path.join(DIR_PATH, 'data/karate.npz')
TEST_CORPUS = os.path.join(DIR_PATH, 'data/corpus.txt.gzip')
TEST_LABELS = np.array(['A', 'B', 'C'])
TEST_CSR = sps.csr_matrix([[0.0, 1.0, 0.0],
 [
  0.0, 0.0, 0.0],
 [
  1.0, 0.0, 0.0]])

def test_normalize_csr_matrix():
    normalized = corpus.normalize_csr_matrix(TEST_CSR)
    @py_assert1 = np.array_equal
    @py_assert4 = normalized.todense
    @py_assert6 = @py_assert4()
    @py_assert9 = TEST_CSR.todense
    @py_assert11 = @py_assert9()
    @py_assert13 = @py_assert1(@py_assert6, @py_assert11)
    if not @py_assert13:
        @py_format15 = ('' + 'assert %(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.todense\n}()\n}, %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s.todense\n}()\n})\n}') % {'py14': @pytest_ar._saferepr(@py_assert13),  'py5': @pytest_ar._saferepr(@py_assert4),  'py10': @pytest_ar._saferepr(@py_assert9),  'py0': @pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py12': @pytest_ar._saferepr(@py_assert11),  'py2': @pytest_ar._saferepr(@py_assert1),  'py7': @pytest_ar._saferepr(@py_assert6),  'py8': @pytest_ar._saferepr(TEST_CSR) if 'TEST_CSR' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TEST_CSR) else 'TEST_CSR',  'py3': @pytest_ar._saferepr(normalized) if 'normalized' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(normalized) else 'normalized'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = None


def test_make_undirected():
    undirected = graph.make_undirected(TEST_CSR)
    @py_assert1 = np.array_equal
    @py_assert4 = undirected.todense
    @py_assert6 = @py_assert4()
    @py_assert8 = [
     [
      0.0, 1.0, 1.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    @py_assert10 = @py_assert1(@py_assert6, @py_assert8)
    if not @py_assert10:
        @py_format12 = ('' + 'assert %(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.todense\n}()\n}, %(py9)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2': @pytest_ar._saferepr(@py_assert1),  'py7': @pytest_ar._saferepr(@py_assert6),  'py3': @pytest_ar._saferepr(undirected) if 'undirected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(undirected) else 'undirected',  'py11': @pytest_ar._saferepr(@py_assert10)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None


def test_random_walks():
    normalized = corpus.normalize_csr_matrix(TEST_CSR)
    random_walks, vocab_cnt = corpus.walk_random(normalized, TEST_LABELS, walk_length=3)
    @py_assert1 = np.array_equal
    @py_assert4 = [
     [
      'A', 'B', ''], ['B', '', ''], ['C', 'A', 'B']]
    @py_assert6 = @py_assert1(random_walks, @py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py3)s, %(py5)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1),  'py7': @pytest_ar._saferepr(@py_assert6),  'py3': @pytest_ar._saferepr(random_walks) if 'random_walks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(random_walks) else 'random_walks',  'py0': @pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert1 = np.array_equal
    @py_assert4 = [
     2, 3, 1]
    @py_assert6 = @py_assert1(vocab_cnt, @py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py3)s, %(py5)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1),  'py7': @pytest_ar._saferepr(@py_assert6),  'py3': @pytest_ar._saferepr(vocab_cnt) if 'vocab_cnt' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(vocab_cnt) else 'vocab_cnt',  'py0': @pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = @py_assert6 = None


def test_walk_graph():
    random_walks, word_freq = corpus.walk_graph(TEST_CSR, TEST_LABELS, walk_length=3, num_walks=2)
    @py_assert1 = np.array_equal
    @py_assert4 = [
     [
      'A', 'B', ''], ['B', '', ''], ['C', 'A', 'B'], ['A', 'B', ''], ['B', '', ''], ['C', 'A', 'B']]
    @py_assert6 = @py_assert1(random_walks, @py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py3)s, %(py5)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1),  'py7': @pytest_ar._saferepr(@py_assert6),  'py3': @pytest_ar._saferepr(random_walks) if 'random_walks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(random_walks) else 'random_walks',  'py0': @pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert2 = {'A': 4,  'B': 6,  'C': 2}
    @py_assert1 = word_freq == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (word_freq, @py_assert2)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(word_freq) if 'word_freq' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(word_freq) else 'word_freq'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_encode_edges():
    edges = np.array([['A', 'B'],
     [
      'A', 'C'],
     [
      'B', 'C'],
     [
      'B', 'E']])
    nodes = np.unique(edges)
    encoded = graph.encode_edges(edges, nodes)
    @py_assert1 = np.array_equal
    @py_assert4 = [
     [
      0, 1], [0, 2], [1, 2], [1, 3]]
    @py_assert6 = @py_assert1(encoded, @py_assert4)
    if not @py_assert6:
        @py_format8 = ('' + 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py3)s, %(py5)s)\n}') % {'py2': @pytest_ar._saferepr(@py_assert1),  'py7': @pytest_ar._saferepr(@py_assert6),  'py3': @pytest_ar._saferepr(encoded) if 'encoded' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(encoded) else 'encoded',  'py0': @pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py5': @pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = @py_assert6 = None


def test_build_adjacency_matrix():
    edges = np.array([['A', 'B'],
     [
      'A', 'C'],
     [
      'B', 'C'],
     [
      'B', 'E']])
    csr_matrix, id2item = graph.build_adjacency_matrix(edges)
    @py_assert2 = len(id2item)
    @py_assert5 = 4
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py3': @pytest_ar._saferepr(@py_assert2),  'py1': @pytest_ar._saferepr(id2item) if 'id2item' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(id2item) else 'id2item',  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = np.array_equal
    @py_assert4 = csr_matrix.todense
    @py_assert6 = @py_assert4()
    @py_assert8 = [
     [
      0.0, 1.0, 1.0, 0.0], [0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]
    @py_assert10 = @py_assert1(@py_assert6, @py_assert8)
    if not @py_assert10:
        @py_format12 = ('' + 'assert %(py11)s\n{%(py11)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.todense\n}()\n}, %(py9)s)\n}') % {'py5': @pytest_ar._saferepr(@py_assert4),  'py9': @pytest_ar._saferepr(@py_assert8),  'py0': @pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2': @pytest_ar._saferepr(@py_assert1),  'py7': @pytest_ar._saferepr(@py_assert6),  'py3': @pytest_ar._saferepr(csr_matrix) if 'csr_matrix' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(csr_matrix) else 'csr_matrix',  'py11': @pytest_ar._saferepr(@py_assert10)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None


def test_load_edges():
    edges = io.load_edges(KARATE_EDGELIST, delimiter=' ', has_header=False)
    @py_assert1 = np.array_equal
    @py_assert3 = edges[0]
    @py_assert5 = [
     '1', '32']
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    if not @py_assert7:
        @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py4)s, %(py6)s)\n}') % {'py8': @pytest_ar._saferepr(@py_assert7),  'py2': @pytest_ar._saferepr(@py_assert1),  'py4': @pytest_ar._saferepr(@py_assert3),  'py0': @pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = edges.shape
    @py_assert4 = (78, 2)
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.shape\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(edges) if 'edges' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(edges) else 'edges'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


@mock.patch('jwalk.io.PANDAS_INSTALLED', False)
def test_load_edges_no_pandas():
    edges = io.load_edges(KARATE_EDGELIST, delimiter=' ')
    @py_assert1 = np.array_equal
    @py_assert3 = edges[0]
    @py_assert5 = [
     '1', '32']
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    if not @py_assert7:
        @py_format9 = ('' + 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.array_equal\n}(%(py4)s, %(py6)s)\n}') % {'py8': @pytest_ar._saferepr(@py_assert7),  'py2': @pytest_ar._saferepr(@py_assert1),  'py4': @pytest_ar._saferepr(@py_assert3),  'py0': @pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = edges.shape
    @py_assert4 = (78, 2)
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.shape\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(edges) if 'edges' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(edges) else 'edges'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_build_corpus():
    with tempfile.NamedTemporaryFile() as (f):
        random_walks, word_freqs = corpus.walk_graph(TEST_CSR, TEST_LABELS)
        corpus_path = corpus.build_corpus(random_walks, outpath=f.name)
        @py_assert3 = f.name
        @py_assert1 = corpus_path == @py_assert3
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s.name\n}', ), (corpus_path, @py_assert3)) % {'py2': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f',  'py4': @pytest_ar._saferepr(@py_assert3),  'py0': @pytest_ar._saferepr(corpus_path) if 'corpus_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(corpus_path) else 'corpus_path'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None


def test_train_model():
    model = skipgram.train_model(TEST_CORPUS, size=50, window=5)
    @py_assert2 = model.wv
    @py_assert4 = @py_assert2.vocab
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 31
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.wv\n}.vocab\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py10': @pytest_ar._saferepr(@py_assert9),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py3': @pytest_ar._saferepr(@py_assert2),  'py7': @pytest_ar._saferepr(@py_assert6),  'py1': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = model.window
    @py_assert4 = 5
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.window\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = model.vector_size
    @py_assert4 = 50
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.vector_size\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = model.sg
    @py_assert4 = 1
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.sg\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_train_skipgram():
    walk_length = 4
    num_walks = 2
    corpus_count = num_walks * len(TEST_LABELS)
    random_walks, word_freq = corpus.walk_graph(TEST_CSR, TEST_LABELS, walk_length, num_walks)
    with tempfile.NamedTemporaryFile() as (f):
        corpus.build_corpus(random_walks, outpath=f.name)
        model = skipgram.train_model(f.name, size=50, window=5, word_freq=word_freq, corpus_count=corpus_count)
        @py_assert2 = model.wv
        @py_assert4 = @py_assert2.vocab
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 3
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.wv\n}.vocab\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py10': @pytest_ar._saferepr(@py_assert9),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py3': @pytest_ar._saferepr(@py_assert2),  'py7': @pytest_ar._saferepr(@py_assert6),  'py1': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model'}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
        @py_assert1 = model.window
        @py_assert4 = 5
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.window\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = model.vector_size
        @py_assert4 = 50
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.vector_size\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(model) if 'model' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(model) else 'model'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None


def test_jwalk():
    with tempfile.NamedTemporaryFile() as (f):
        res = __main__.jwalk(KARATE_EDGELIST, outfile=f.name, delimiter=' ')
        @py_assert3 = f.name
        @py_assert1 = res == @py_assert3
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s.name\n}', ), (res, @py_assert3)) % {'py2': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f',  'py4': @pytest_ar._saferepr(@py_assert3),  'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None


def test_online():
    with tempfile.NamedTemporaryFile() as (f):
        res = __main__.jwalk(KARATE_EDGELIST, outfile=f.name, delimiter=' ', model_path=KARATE_EMBEDDINGS)
        @py_assert3 = f.name
        @py_assert1 = res == @py_assert3
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s.name\n}', ), (res, @py_assert3)) % {'py2': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f',  'py4': @pytest_ar._saferepr(@py_assert3),  'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None


def test_adjacency():
    with tempfile.NamedTemporaryFile() as (f):
        res = __main__.jwalk(KARATE_GRAPH, outfile=f.name, delimiter=' ')
        @py_assert3 = f.name
        @py_assert1 = res == @py_assert3
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s.name\n}', ), (res, @py_assert3)) % {'py2': @pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f',  'py4': @pytest_ar._saferepr(@py_assert3),  'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None


def test_parser():
    parser = __main__.create_parser()
    args = parser.parse_args(['--input', 'infile', '--output', 'outfile'])
    @py_assert1 = args.infile
    @py_assert4 = 'infile'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.infile\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = args.outfile
    @py_assert4 = 'outfile'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.outfile\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1),  'py5': @pytest_ar._saferepr(@py_assert4),  'py0': @pytest_ar._saferepr(args) if 'args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(args) else 'args'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None