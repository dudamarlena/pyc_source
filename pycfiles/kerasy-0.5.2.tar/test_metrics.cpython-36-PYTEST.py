# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/test_metrics.py
# Compiled at: 2020-05-13 02:52:50
# Size of source mod 2**32: 919 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, numpy as np
from kerasy import metrics
n_features = 5
y_shape_ = np.ones(shape=(5, ))
y_shape_1 = np.ones(shape=(1, n_features))
y_shape_10 = np.ones(shape=(10, 5))

def metrics_check(metric, y):
    loss = metric.loss(y, y)
    @py_assert1 = []
    @py_assert5 = isinstance(loss, float)
    @py_assert0 = @py_assert5
    if not @py_assert5:
        @py_assert11 = isinstance(loss, int)
        @py_assert0 = @py_assert11
    if not @py_assert0:
        @py_format7 = '%(py6)s\n{%(py6)s = %(py2)s(%(py3)s, %(py4)s)\n}' % {'py2':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py3':@pytest_ar._saferepr(loss) if 'loss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(loss) else 'loss',  'py4':@pytest_ar._saferepr(float) if 'float' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(float) else 'float',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_assert1.append(@py_format7)
        if not @py_assert5:
            @py_format13 = '%(py12)s\n{%(py12)s = %(py8)s(%(py9)s, %(py10)s)\n}' % {'py8':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py9':@pytest_ar._saferepr(loss) if 'loss' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(loss) else 'loss',  'py10':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py12':@pytest_ar._saferepr(@py_assert11)}
            @py_assert1.append(@py_format13)
        @py_format14 = @pytest_ar._format_boolop(@py_assert1, 1) % {}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert0 = @py_assert1 = @py_assert5 = @py_assert11 = None


def _test_metrics(identifier):
    metric = metrics.get(identifier)
    metrics_check(metric, y_shape_)
    metrics_check(metric, y_shape_1)
    metrics_check(metric, y_shape_10)


def test_categorical_accuracy():
    _test_metrics(identifier='categorical_accuracy')


def test_mean_squared_error():
    _test_metrics(identifier='mean_squared_error')


def test_mse():
    _test_metrics(identifier='mse')


def test_categorical_crossentropy():
    _test_metrics(identifier='categorical_crossentropy')


def test_softmax_categorical_crossentropy():
    _test_metrics(identifier='softmax_categorical_crossentropy')