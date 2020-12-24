# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhetherly/Projects/linear_binning/linear_binning/test/test_linear_binning.py
# Compiled at: 2017-10-03 16:21:57
# Size of source mod 2**32: 2452 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from linear_binning import linear_binning
import numpy as np, logging
from timeit import default_timer as timer
logging.basicConfig(level=(logging.INFO))

def generate_data(n_samples=100000, D=2):
    sample_coords = np.random.random(size=(n_samples, D))
    sample_weights = np.random.random(size=n_samples)
    extents = np.tile([0.02, 0.8999], D).reshape((D, 2))
    sizes = np.full(D, 51)
    return (
     sample_coords, sample_weights, extents, sizes)


def test_sum_of_weights():
    sample_coords, sample_weights, extents, sizes = generate_data(1000000)
    start = timer()
    coords, weights = linear_binning(sample_coords, sample_weights, extents, sizes)
    end = timer()
    logging.info('\n')
    logging.info('One million 2D points binned with linear_binning in {}s'.format(end - start))
    @py_assert1 = np.allclose
    @py_assert4 = weights.sum
    @py_assert6 = @py_assert4()
    @py_assert9 = sample_weights.sum
    @py_assert11 = @py_assert9()
    @py_assert13 = @py_assert1(@py_assert6, @py_assert11)
    if not @py_assert13:
        @py_format15 = ('' + 'assert %(py14)s\n{%(py14)s = %(py2)s\n{%(py2)s = %(py0)s.allclose\n}(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.sum\n}()\n}, %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s.sum\n}()\n})\n}') % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(weights) if 'weights' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weights) else 'weights',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(sample_weights) if 'sample_weights' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sample_weights) else 'sample_weights',  'py10':@pytest_ar._saferepr(@py_assert9),  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert9 = @py_assert11 = @py_assert13 = None
    x = np.ascontiguousarray(sample_coords[:, 0])
    y = np.ascontiguousarray(sample_coords[:, 1])
    start = timer()
    np.histogram2d(x, y, weights=sample_weights,
      bins=sizes,
      range=extents)
    end = timer()
    logging.info('For comparison, np.histogram2d finished in {}s'.format(end - start))
    sample_coords = np.array([[0.2, 0.9], [0.5, 1.1], [-0.1, 0.7]])
    sample_weights = np.array([25, 50, 25])
    extents = np.array([[0.0, 1.0], [0.0, 1.0]])
    sizes = np.array([11, 11])
    coords, weights = linear_binning(sample_coords, sample_weights, extents, sizes)
    pass_value_test = True
    value_tests = 0
    for i in range(coords.shape[0]):
        if np.allclose(coords[(i, 0)], 0.0):
            if np.allclose(coords[(i, 1)], 0.7):
                pass_value_test &= np.allclose(weights[i], 25.0)
                value_tests += 1
        elif np.allclose(coords[(i, 0)], 0.2):
            if np.allclose(coords[(i, 1)], 0.9):
                pass_value_test &= np.allclose(weights[i], 25.0)
                value_tests += 1
        elif np.allclose(coords[(i, 0)], 0.5):
            if np.allclose(coords[(i, 1)], 1.0):
                pass_value_test &= np.allclose(weights[i], 50.0)
                value_tests += 1
        else:
            pass_value_test &= np.allclose(weights[i], 0.0)

    @py_assert1 = []
    @py_assert0 = pass_value_test
    if pass_value_test:
        @py_assert6 = 3
        @py_assert5 = value_tests == @py_assert6
        @py_assert0 = @py_assert5
    if not @py_assert0:
        @py_format3 = '%(py2)s' % {'py2': @pytest_ar._saferepr(pass_value_test) if 'pass_value_test' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pass_value_test) else 'pass_value_test'}
        @py_assert1.append(@py_format3)
        if pass_value_test:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s == %(py7)s', ), (value_tests, @py_assert6)) % {'py4':@pytest_ar._saferepr(value_tests) if 'value_tests' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value_tests) else 'value_tests',  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = '%(py9)s' % {'py9': @py_format8}
            @py_assert1.append(@py_format10)
        @py_format11 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert0 = @py_assert1 = @py_assert5 = @py_assert6 = None