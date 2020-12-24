# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/test_initializers.py
# Compiled at: 2020-05-13 02:32:05
# Size of source mod 2**32: 3146 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from kerasy.models import Sequential
from kerasy.layers import Input, Conv2D, Dense
square_matrix_size = (10, 10)
kh, kw = (3, 3)
F, OF = (5, 8)

def _test_initialization_conv(kernel_initializer):
    model = Sequential()
    model.add(Input(input_shape=(20, 20, F)))
    model.add(Conv2D(filters=OF, kernel_size=(kh, kw), kernel_initializer=kernel_initializer))
    model.compile(loss='mse', optimizer='adam')
    @py_assert0 = model.layers[(-1)]
    @py_assert2 = @py_assert0.kernel
    @py_assert4 = @py_assert2.shape
    @py_assert7 = (
     kh, kw, F, OF)
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.kernel\n}.shape\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def _test_initialization_dense(kernel_initializer):
    units_in, units_out = square_matrix_size
    model = Sequential()
    model.add(Input(input_shape=units_in))
    model.add(Dense(units_out, kernel_initializer=kernel_initializer))
    model.compile(loss='mse', optimizer='adam')
    @py_assert0 = model.layers[(-1)]
    @py_assert2 = @py_assert0.kernel
    @py_assert4 = @py_assert2.shape
    @py_assert6 = @py_assert4 == square_matrix_size
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.kernel\n}.shape\n} == %(py7)s', ), (@py_assert4, square_matrix_size)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(square_matrix_size) if 'square_matrix_size' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(square_matrix_size) else 'square_matrix_size'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


def test_zeros():
    _test_initialization_conv(kernel_initializer='zeros')
    _test_initialization_dense(kernel_initializer='zeros')


def test_ones():
    _test_initialization_conv(kernel_initializer='ones')
    _test_initialization_dense(kernel_initializer='ones')


def test_constant():
    _test_initialization_conv(kernel_initializer='constant')
    _test_initialization_dense(kernel_initializer='constant')


def test_random_normal():
    _test_initialization_conv(kernel_initializer='random_normal')
    _test_initialization_dense(kernel_initializer='random_normal')


def test_random_uniform():
    _test_initialization_conv(kernel_initializer='random_uniform')
    _test_initialization_dense(kernel_initializer='random_uniform')


def test_truncated_normal():
    _test_initialization_conv(kernel_initializer='truncated_normal')
    _test_initialization_dense(kernel_initializer='truncated_normal')


def test_variance_scaling():
    _test_initialization_conv(kernel_initializer='variance_scaling')
    _test_initialization_dense(kernel_initializer='variance_scaling')


def test_orthogonal():
    _test_initialization_conv(kernel_initializer='orthogonal')
    _test_initialization_dense(kernel_initializer='orthogonal')


def test_identity():
    _test_initialization_dense(kernel_initializer='identity')


def test_glorot_normal():
    _test_initialization_conv(kernel_initializer='glorot_normal')
    _test_initialization_dense(kernel_initializer='glorot_normal')


def test_glorot_uniform():
    _test_initialization_conv(kernel_initializer='glorot_uniform')
    _test_initialization_dense(kernel_initializer='glorot_uniform')


def test_he_normal():
    _test_initialization_conv(kernel_initializer='he_normal')
    _test_initialization_dense(kernel_initializer='he_normal')


def test_lecun_normal():
    _test_initialization_conv(kernel_initializer='lecun_normal')
    _test_initialization_dense(kernel_initializer='lecun_normal')


def test_he_uniform():
    _test_initialization_conv(kernel_initializer='he_uniform')
    _test_initialization_dense(kernel_initializer='he_uniform')


def test_lecun_uniform():
    _test_initialization_conv(kernel_initializer='lecun_uniform')
    _test_initialization_dense(kernel_initializer='lecun_uniform')