# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/ML/test_sampling.py
# Compiled at: 2020-05-13 03:44:35
# Size of source mod 2**32: 538 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from kerasy.ML.sampling import GibbsMsphereSampler

def test_gibbs_msphere_sampling(target=0.15):
    radius = 10
    num_samples = 10000
    dimension = 6
    sampler = GibbsMsphereSampler(dimension=dimension, radius=radius)
    sample = sampler.sample(num_samples, verbose=(-1))
    norm = np.sum((np.square(sample)), axis=1)
    actual = np.count_nonzero(norm <= (radius / 2) ** 2)
    ideal = 0.5 ** dimension * num_samples
    @py_assert1 = np.all
    @py_assert6 = 2
    @py_assert8 = radius ** @py_assert6
    @py_assert4 = norm <= @py_assert8
    @py_assert11 = @py_assert1(@py_assert4)
    if not @py_assert11:
        @py_format9 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert4,), ('%(py3)s <= (%(py5)s ** %(py7)s)', ), (norm, @py_assert8)) % {'py3':@pytest_ar._saferepr(norm) if 'norm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(norm) else 'norm',  'py5':@pytest_ar._saferepr(radius) if 'radius' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(radius) else 'radius',  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s\n{%(py12)s = %(py2)s\n{%(py2)s = %(py0)s.all\n}(%(py10)s)\n}' % {'py0':@pytest_ar._saferepr(np) if 'np' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(np) else 'np',  'py2':@pytest_ar._saferepr(@py_assert1),  'py10':@py_format9,  'py12':@pytest_ar._saferepr(@py_assert11)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert11 = None
    @py_assert3 = actual / ideal
    @py_assert4 = 1
    @py_assert6 = @py_assert3 - @py_assert4
    @py_assert7 = abs(@py_assert6)
    @py_assert9 = @py_assert7 <= target
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('<=', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py0)s(((%(py1)s / %(py2)s) - %(py5)s))\n} <= %(py10)s', ), (@py_assert7, target)) % {'py0':@pytest_ar._saferepr(abs) if 'abs' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(abs) else 'abs',  'py1':@pytest_ar._saferepr(actual) if 'actual' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(actual) else 'actual',  'py2':@pytest_ar._saferepr(ideal) if 'ideal' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ideal) else 'ideal',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(target) if 'target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(target) else 'target'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert3 = @py_assert4 = @py_assert6 = @py_assert7 = @py_assert9 = None