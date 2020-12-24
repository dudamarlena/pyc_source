# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrival/__init__.py
# Compiled at: 2019-07-28 05:29:59
# Size of source mod 2**32: 8269 bytes
import builtins.as_integer_ratio as as_integer_ratio
import builtins.bootstrap as bootstrap
from builtins.FastIO import FastIO, IOWrapper, input
from builtins.heap import Heap, OrderHeap, RemovalHeap, XHeap
import builtins.mergesort as mergesort
import builtins.split as split
import builtins.tree_repr as tree_repr
from performance.bit_hacks import least_bit, next_mask, subset_masks, sum_of_subsets
from performance.memoize import memodict, memoize
from performance.ostream import cout, endl, ostream
import performance.readnumbers as readnumbers
from snippets.algebra import ntt
from snippets.algebra.chinese_remainder import chinese_remainder, composite_crt
import snippets.algebra.discrete_log as discrete_log
from snippets.algebra.factors import all_factors, distinct_factors, pollard_rho, prime_factors
from snippets.algebra.fft import fft, fft_conv
from snippets.algebra.fst import fst, fst_conv
from snippets.algebra.gcd import extended_gcd, gcd, gcdm, lcm, lcmm
import snippets.algebra.is_prime as is_prime
import snippets.algebra.mod_sqrt as mod_sqrt
import snippets.algebra.modinv as modinv
import snippets.algebra.phi as phi
from snippets.algebra.primitive_root import ilog, primitive_root
from snippets.algebra.sieve import prime_list, prime_sieve
from snippets.combinatorics.combinatorics import catalan_recursive, euler_recursive, stirling_1_recursive, stirling_2_recursive
from snippets.combinatorics.nCr_mod import make_nCr_mod
from snippets.combinatorics.partitions import partition
from snippets.data_structures.BitArray import bitarray
from snippets.data_structures.CFraction import CFrac2Frac, CFraction
from snippets.data_structures.DisjointSetUnion import DisjointSetUnion, UnionFind
import snippets.data_structures.FenwickTree as FenwickTree
from snippets.data_structures.Fraction import Fraction, limit_denominator
import snippets.data_structures.LazySegmentTree as LazySegmentTree
import snippets.data_structures.LinkedList as LinkedList
import snippets.data_structures.Node as Node
from snippets.data_structures.PersistentSegTree import create, minimum, setter
import snippets.data_structures.RangeQuery as RangeQuery
import snippets.data_structures.SegmentTree as SegmentTree
import snippets.data_structures.SortedList as SortedList
from snippets.data_structures.Treap import TreapHashMap, TreapHashSet, TreapMultiSet, TreapSet, treap_builder, treap_ceiling, treap_create_node, treap_erase, treap_floor, treap_higher, treap_insert, treap_insert_unique, treap_keys, treap_lower, treap_max, treap_merge, treap_min, treap_prior, treap_split
import snippets.data_structures.Trie as Trie
import snippets.data_structures.TwoSat as TwoSat
import snippets.geometry.convex_hull as convex_hull
from snippets.geometry.lines import collinear, dist, get_2dline, intersect, is_parallel, is_same, rotate
from snippets.geometry.vectors import angle, closest_point, cross2d, cross3d, dot, norm_sq, scale, to_vec, translate
import snippets.graphs.bellman_ford as bellman_ford
from snippets.graphs.bfs import bfs, layers
from snippets.graphs.components import connected_components
import snippets.graphs.cycle_finding as cycle_finding
import snippets.graphs.dfs as dfs
import snippets.graphs.dijkstra as dijkstra
from snippets.graphs.dinic import Dinic
import snippets.graphs.euler_walk as euler_walk
import snippets.graphs.find_path as find_path
import snippets.graphs.floyd_warshall as floyd_warshall
import snippets.graphs.is_bipartite as is_bipartite
import snippets.graphs.kruskal as kruskal
from snippets.graphs.lca import LCA
import snippets.graphs.prim as prim
import snippets.graphs.scc as scc
from snippets.graphs.toposort import kahn, toposort
from snippets.linear_algebra.matrix import eye, mat_add, mat_inv, mat_mul, mat_pow, mat_sub, minor, transpose, vec_mul
from snippets.linear_algebra.multivariable_crt import is_sol, mcrt, pivot
from snippets.misc.alphabeta import AlphaBetaNode, alphabeta
import snippets.misc.cumsum2d as cumsum2d
import snippets.misc.lis as lis
import snippets.misc.order_statistic as order_statistic
from snippets.numerical import berlekamp_massey
import snippets.numerical.hill_climbing as hill_climbing
from snippets.numerical.integrate import fast_quad, quad, rec, simpson
import snippets.numerical.interpolate as interpolate
import snippets.numerical.iroot as iroot
from snippets.numerical.polynomial import diff, divroot, poly
from snippets.numerical.search import binary_search, discrete_binary_search, discrete_ternary_search, fractional_binary_search, golden_section_search, ternary_search
from snippets.strings.hashing import Hashing
from snippets.strings.kmp import match, partial, string_find
import snippets.strings.lcs as lcs
import snippets.strings.LCSubstr as LCSubstr
import snippets.strings.LPSubstr as LPSubstr
from snippets.strings.min_rotation import least_rotation
from .version import version
__version__ = version
__all__ = [
 'AlphaBetaNode',
 'CFrac2Frac',
 'CFraction',
 'Dinic',
 'DisjointSetUnion',
 'FastIO',
 'FenwickTree',
 'Fraction',
 'Hashing',
 'Heap',
 'IOWrapper',
 'LCA',
 'LCSubstr',
 'LPSubstr',
 'LazySegmentTree',
 'LinkedList',
 'Node',
 'OrderHeap',
 'RangeQuery',
 'RemovalHeap',
 'SegmentTree',
 'SortedList',
 'TreapHashMap',
 'TreapHashSet',
 'TreapMultiSet',
 'TreapSet',
 'Trie',
 'TwoSat',
 'UnionFind',
 'XHeap',
 'all_factors',
 'alphabeta',
 'angle',
 'as_integer_ratio',
 'bellman_ford',
 'berlekamp_massey',
 'bfs',
 'binary_search',
 'bitarray',
 'bootstrap',
 'builtins',
 'catalan_recursive',
 'chinese_remainder',
 'closest_point',
 'collinear',
 'composite_crt',
 'connected_components',
 'convex_hull',
 'cout',
 'create',
 'cross2d',
 'cross3d',
 'cumsum2d',
 'cycle_finding',
 'dfs',
 'diff',
 'dijkstra',
 'discrete_binary_search',
 'discrete_log',
 'discrete_ternary_search',
 'dist',
 'distinct_factors',
 'divroot',
 'dot',
 'endl',
 'euler_recursive',
 'euler_walk',
 'extended_gcd',
 'eye',
 'fast_quad',
 'fft',
 'fft_conv',
 'find_path',
 'floyd_warshall',
 'fractional_binary_search',
 'fst',
 'fst_conv',
 'gcd',
 'gcdm',
 'get_2dline',
 'golden_section_search',
 'hill_climbing',
 'ilog',
 'input',
 'interpolate',
 'intersect',
 'iroot',
 'is_bipartite',
 'is_parallel',
 'is_prime',
 'is_same',
 'is_sol',
 'kahn',
 'kruskal',
 'layers',
 'lcm',
 'lcmm',
 'lcs',
 'least_bit',
 'least_rotation',
 'limit_denominator',
 'lis',
 'make_nCr_mod',
 'mat_add',
 'mat_inv',
 'mat_mul',
 'mat_pow',
 'mat_sub',
 'match',
 'mcrt',
 'memodict',
 'memoize',
 'mergesort',
 'minimum',
 'minor',
 'mod_sqrt',
 'modinv',
 'next_mask',
 'norm_sq',
 'ntt',
 'order_statistic',
 'ostream',
 'partition',
 'performance',
 'phi',
 'partial',
 'pivot',
 'pollard_rho',
 'poly',
 'prim',
 'prime_factors',
 'prime_list',
 'prime_sieve',
 'primitive_root',
 'quad',
 'readnumbers',
 'rec',
 'rotate',
 'scale',
 'scc',
 'setter',
 'simpson',
 'snippets',
 'split',
 'stirling_1_recursive',
 'stirling_2_recursive',
 'string_find',
 'subset_masks',
 'sum_of_subsets',
 'ternary_search',
 'to_vec',
 'toposort',
 'translate',
 'transpose',
 'treap_builder',
 'treap_ceiling',
 'treap_create_node',
 'treap_erase',
 'treap_floor',
 'treap_higher',
 'treap_insert',
 'treap_insert_unique',
 'treap_keys',
 'treap_lower',
 'treap_max',
 'treap_merge',
 'treap_min',
 'treap_prior',
 'treap_split',
 'tree_repr',
 'vec_mul']