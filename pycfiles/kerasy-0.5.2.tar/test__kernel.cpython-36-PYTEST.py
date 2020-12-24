# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/ML/test__kernel.py
# Compiled at: 2020-05-11 06:58:16
# Size of source mod 2**32: 1396 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from kerasy.ML import _kernel

def get_test_data():
    rnd = np.random.RandomState(123)
    x, y = rnd.rand(2, 10)
    return (x, y)


def _test_kernel(kernel):
    x, y = get_test_data()
    kernel = _kernel.get(kernel)
    val = kernel(x, y)
    @py_assert1 = []
    @py_assert5 = isinstance(val, int)
    @py_assert0 = @py_assert5
    if not @py_assert5:
        @py_assert11 = isinstance(val, float)
        @py_assert0 = @py_assert11
    if not @py_assert0:
        @py_format7 = '%(py6)s\n{%(py6)s = %(py2)s(%(py3)s, %(py4)s)\n}' % {'py2':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py3':@pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val',  'py4':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_assert1.append(@py_format7)
        if not @py_assert5:
            @py_format13 = '%(py12)s\n{%(py12)s = %(py8)s(%(py9)s, %(py10)s)\n}' % {'py8':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py9':@pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val',  'py10':@pytest_ar._saferepr(float) if 'float' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(float) else 'float',  'py12':@pytest_ar._saferepr(@py_assert11)}
            @py_assert1.append(@py_format13)
        @py_format14 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert0 = @py_assert1 = @py_assert5 = @py_assert11 = None


def test_linear():
    Linear = _kernel.get('linear', c=0)
    _test_kernel(Linear)


def test_polynomial():
    Polynomial = _kernel.get('polynomial', alpha=1, c=0, d=3)
    _test_kernel(Polynomial)


def test_gaussian():
    Gaussian = _kernel.get('gaussian', sigma=1)
    _test_kernel(Gaussian)


def test_exponential():
    Exponential = _kernel.get('exponential', sigma=0.1)
    _test_kernel(Exponential)


def test_laplacian():
    Laplacian = _kernel.get('laplacian', sigma=0.1)
    _test_kernel(Laplacian)


def test_sigmoid():
    Sigmoid = _kernel.get('sigmoid', alpha=1, c=0)
    _test_kernel(Sigmoid)


def test_rational_quadratic():
    Rational_quadratic = _kernel.get('rational_quadratic', c=1)
    _test_kernel(Rational_quadratic)


def test_multiquadric():
    Multiquadric = _kernel.get('multiquadric', c=1)
    _test_kernel(Multiquadric)


def test_inverse_multiquadric():
    Inverse_multiquadric = _kernel.get('inverse_multiquadric', c=1)
    _test_kernel(Inverse_multiquadric)


def test_log():
    Log = _kernel.get('log', d=3)
    _test_kernel(Log)