# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/test_losses.py
# Compiled at: 2020-05-13 02:50:36
# Size of source mod 2**32: 858 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from kerasy import losses
n_features = 5
y_shape_ = np.ones(shape=(5, ))
y_shape_1 = np.ones(shape=(1, n_features))
y_shape_10 = np.ones(shape=(10, 5))

def loss_check(loss, y):
    val = loss.loss(y, y)
    @py_assert1 = []
    @py_assert5 = isinstance(val, float)
    @py_assert0 = @py_assert5
    if not @py_assert5:
        @py_assert11 = isinstance(val, int)
        @py_assert0 = @py_assert11
    if not @py_assert0:
        @py_format7 = '%(py6)s\n{%(py6)s = %(py2)s(%(py3)s, %(py4)s)\n}' % {'py2':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py3':@pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val',  'py4':@pytest_ar._saferepr(float) if 'float' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(float) else 'float',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_assert1.append(@py_format7)
        if not @py_assert5:
            @py_format13 = '%(py12)s\n{%(py12)s = %(py8)s(%(py9)s, %(py10)s)\n}' % {'py8':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py9':@pytest_ar._saferepr(val) if 'val' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(val) else 'val',  'py10':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py12':@pytest_ar._saferepr(@py_assert11)}
            @py_assert1.append(@py_format13)
        @py_format14 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert0 = @py_assert1 = @py_assert5 = @py_assert11 = None
    diff = loss.diff(y, y)
    @py_assert1 = diff.shape
    @py_assert5 = y.shape
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.shape\n} == %(py6)s\n{%(py6)s = %(py4)s.shape\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(diff) if 'diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(diff) else 'diff',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(y) if 'y' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(y) else 'y',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def _test_losses(identifier):
    loss = losses.get(identifier)
    loss_check(loss, y_shape_)
    loss_check(loss, y_shape_1)
    loss_check(loss, y_shape_10)


def test_mean_squared_error():
    _test_losses(identifier='mean_squared_error')


def test_mse():
    _test_losses(identifier='mse')


def test_categorical_crossentropy():
    _test_losses(identifier='categorical_crossentropy')


def test_softmax_categorical_crossentropy():
    _test_losses(identifier='softmax_categorical_crossentropy')